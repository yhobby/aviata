import aioredis
from sanic import Sanic
from sanic_jinja2 import SanicJinja2

from src.worker import generate_unique_routes

app = Sanic(__name__)
jinja = SanicJinja2(app)


@app.route('/')
@jinja.template('index.html')
async def index(request):
    db = await aioredis.create_redis_pool('redis://redis')
    routes = generate_unique_routes()
    data = {}
    for route in routes:
        data[route] = await db.hgetall(route, encoding='utf-8')
    return {'data': data}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
