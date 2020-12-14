import itertools

import redis
from celery import Celery
from celery.schedules import crontab

from src.api import search_flights, check_flights
from src.settings import IATA_CODES

db = redis.Redis(host='redis')
app = Celery(broker='redis://redis:6379/1')

app.conf.timezone = 'Asia/Almaty'
app.conf.beat_schedule = {
    'midnight_updates': {
        'task': 'src.worker.midnight_updates',
        'schedule': crontab(minute=0, hour=0) # Execute daily at midnight.
    },
    'price_confirmations': {
        'task': 'src.worker.price_confirmations',
        'schedule': crontab() # Execute every minutes
    },
}


# Execute daily at midnight.
@app.task()
def midnight_updates():
    routes = generate_unique_routes()
    for route in routes:
        data = search_flights(route)
        print('midnight_updates', f'{route=}')
        for key, value in data.items():
            db.hset(key, None, None, value)


# Execute every minutes.
@app.task()
def price_confirmations():
    routes = generate_unique_routes()
    for route in routes:
        try:
            token = db.hget(route, 'booking_token').decode('utf-8')
            status = check_flights(token)
            print('price_confirmations', f'{route=}')
            db.hset(route, 'status', status)
        except AttributeError:
            print('This direction is absent in the database, please wait we will fill the DB')
            data = search_flights(route)
            print('midnight_updates', f'{route=}')
            for key, value in data.items():
                db.hset(key, None, None, value)


def generate_unique_routes(codes=IATA_CODES) -> list:
    directions = itertools.permutations(codes, 2)
    result = []
    for d in directions:
        result.append(d[0] + '_' + d[1])  # Generate 'FROM_TO'
    return result