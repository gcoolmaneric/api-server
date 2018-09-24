import logging
import json

from decimal import Decimal
from datetime import datetime
from flask import make_response, redirect

TIME_ZERO = datetime.utcfromtimestamp(0)


def pack_custom_response(data_list):
    '''
    Pack proper responsed data in json for APIs
    '''
    response_data = {}
    items = []
    items_dict = {}
    shops = []
    shops_dict = {}

    for data in data_list:
        if data.get('title') and data.get('id'):
            if data.get('id') not in shops_dict:
                shops_dict[data.get('id')] = data
                shops.append(data)

        if data.get('name') and data.get('id'):
            if data.get('id') not in items_dict:
                items_dict[data.get('id')] = data
                items.append(data)

    if items:
        response_data['items'] = items

    if shops:
        response_data['shopping_list'] = shops

    return response_data


def json_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)

    if isinstance(obj, datetime):
        return int((obj - TIME_ZERO).total_seconds() * 1000)

    if hasattr(obj, 'to_json'):
        return obj.to_json()

    raise TypeError


def normalize(obj):
    return json.loads(json.dumps(obj, default=json_serializer))


def render_error(error, description):
    error_code = {
        'invalid_request':             400,
        'invalid_items':               404,
        'data_does_not_exist':         404,
        'unknown_method':              405,
        'too_many_requests':           429,
        'internal_server_error':       500,
        'unimplemented':               500,
    }

    response = make_response(json.dumps({'status': error_code.get(error), 'reason': description}))
    response.status_code = error_code.get(error)
    response.headers["Content-Type"] = "application/json"

    logging.error('error status: %s reason: %s', error_code.get(error), description)

    return response


def render_response(code, resp_data):
    response = None

    if not isinstance(resp_data, str):
        response = make_response(json.dumps(
            {'status': code, 'data': resp_data}, default=json_serializer))
    else:
        response = make_response(json.dumps({'status': code, 'data': resp_data}))

    response.headers["Content-Type"] = "application/json"

    return response
