import json
import datetime

import requests

from src.settings import URL_FOR_SEARCH, HEADERS, URL_FOR_CHECK, PARTNER, AFFILY


############################
# PART-1. MIDNIGHT UPDATES #
############################

def time_span_generation(days=30) -> tuple:
    date_from = datetime.date.today()
    date_to = date_from + datetime.timedelta(days=days)
    return date_from.strftime('%d/%m/%Y'), date_to.strftime('%d/%m/%Y')


def get_cheapest_cost(direction: tuple) -> tuple:
    date_from, date_to = time_span_generation()
    fly_from, fly_to = direction.split('_')

    url = URL_FOR_SEARCH
    headers = HEADERS
    payload = {
        'fly_from': f'{fly_from}',
        'fly_to': f'{fly_to}',
        'date_from': f'{date_from}',
        'date_to': f'{date_to}',
        'partner': PARTNER,
        'adults': 1
    }
    try:
        response = requests.get(url, headers=headers, params=payload)

        if response.status_code == 200:
            dict_data = json.loads(response.text)
            sorted_data = sorted(dict_data['data'], key=lambda x: x['price'])

            date_in_utc = sorted_data[0]['dTimeUTC']
            date = datetime.datetime.fromtimestamp(date_in_utc).strftime('%c')
            print('price', sorted_data[0]['price'])
            return sorted_data[0]['price'], sorted_data[0]['booking_token'], date  # price, token, date flight
        else:
            print('API Error')
    except requests.ConnectionError:
        print('You have problem with network')


def search_flights(route: str) -> tuple:
    price, booking_token, date_flight = get_cheapest_cost(route)
    flight = {
        'route': f'{route}',
        'price': f'{str(price)}',
        'booking_token': f'{booking_token}',
        'status': 'valid',
        'date': f'{date_flight}'
    }
    result = {route: flight}
    return result


###############################
# PART-2. PRICE CONFIRMATIONS #
###############################

def parse_status_data(price_changed_status, flights_status):
    if flights_status == True and price_changed_status == False:
        status = 'valid'
    elif price_changed_status == True:
        status = 'price changed'
    else:
        status = 'invalid'
    return status


def get_flights_status(booking_token):
    url = URL_FOR_CHECK
    headers = HEADERS
    payload = {
        'v': 2,  # API version, use 2
        'booking_token': f'{booking_token}',
        'bnum': 0,  # The number of bags for the booking
        'pnum': 1,  # Number of passengers
        'affily': AFFILY,  # Your affiliate/partner ID
        'adults': 1,
        'children': 0,
        'infants': 0,
    }
    try:
        response = requests.get(url, headers=headers, params=payload)

        if response.status_code == 200:
            dict_data = json.loads(response.text)
            if dict_data['flights_invalid'] == True:
                status = 'invalid'
            else:
                flights_status = dict_data['flights_checked']
                price_changed_status = dict_data['price_change']
                status = parse_status_data(price_changed_status, flights_status)
            return status
        else:
            print('Problem with server API')
    except requests.ConnectionError:
        print('You have problem with network')


def check_flights(token) -> str:
    status = get_flights_status(token)
    return status
