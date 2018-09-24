import logging
import ast

from flask import Blueprint, request
from apiserver.utils.render import render_error, render_response, pack_custom_response
from apiserver.service.shopping_service import ShoppingService

shop = Blueprint('shop', __name__)


@shop.route('/api/v1/create_list', methods=['POST'])
def create_list():
    '''
    Create a shopping list
    '''
    try:
        request_data = request.get_json(force=True)
        if not request_data:
            return render_error('invalid_request', 'request parameters are null')

        name = request_data.get('name', None)
        if not name:
            return render_error('invalid_request', 'name is null')

        title = request_data.get('title', None)
        if not title:
            return render_error('invalid_request', 'title is null')

        data = ShoppingService.create_list(title, name)
        if not data:
            logging.error('failed to create a shopping list')
            return render_error('internal_server_error', 'Internal server error')

        logging.debug('data %s', data)

        return render_response(200, data)

    except Exception as e:
        logging.error(e, exc_info=True)
        return render_error('internal_server_error', "Internal server error")


@shop.route('/api/v1/add_items', methods=['POST'])
def add_items():
    '''
    Add items to a shopping list
    '''
    try:
        request_data = request.get_json(force=True)
        if not request_data:
            return render_error('invalid_request', 'request parameters are null')

        list_id = request_data.get('listId', None)
        if not list_id:
            return render_error('invalid_request', 'list_id is null')

        items = request_data.get('items', None)
        if not items:
            return render_error('invalid_request', 'items are empty')

        data = ShoppingService.get_shop_by_list_id(list_id)
        if not data:
            return render_error('data_does_not_exist', 'cannot find shopping list by list_id')

        status = ShoppingService.add_items(list_id, items)
        if not status:
            return render_error('invalid_items', 'failed to add items')

        data_list = ShoppingService.get_list_by_shop_list_id(list_id)
        if not data_list:
            return render_error('data_does_not_exist', 'failed to update list')

        return render_response(200, pack_custom_response(data_list))

    except Exception as e:
        logging.error(e, exc_info=True)
        return render_error('internal_server_error', "Internal server error")


@shop.route('/api/v1/update_list', methods=['POST'])
def update_list():
    '''
    Update a shopping list's title and name by list_id
    '''
    try:
        request_data = request.get_json(force=True)
        if not request_data:
            return render_error('invalid_request', 'request parameters are null')

        list_id = request_data.get('listId', None)
        if not list_id:
            return render_error('invalid_request', 'list_id is null')

        title = request_data.get('title', None)
        if not title:
            return render_error('invalid_request', 'title is null')

        name = request_data.get('name', None)
        if not name:
            return render_error('invalid_request', 'tinametle is null')

        data = ShoppingService.get_shop_by_list_id(list_id)
        if not data:
            return render_error('data_does_not_exist', 'cannot find shopping list by list_id')

        data = ShoppingService.update_list({'title': title, 'shop_name': name}, list_id)
        if not data:
            return render_error('data_does_not_exist', 'shopping list is null')

        return render_response(200, data)

    except Exception as e:
        logging.error(e, exc_info=True)
        return render_error('internal_server_error', "Internal server error")


@shop.route('/api/v1/delete_list', methods=['POST'])
def delete_list():
    '''
    Delete a shopping list by list_id
    '''
    try:
        request_data = request.get_json(force=True)
        if not request_data:
            return render_error('invalid_request', 'request parameters are null')

        list_id = request_data.get('listId', None)
        if not list_id:
            return render_error('invalid_request', 'list_id is null')

        data = ShoppingService.get_shop_by_list_id(list_id)
        if not data:
            return render_error('data_does_not_exist', 'cannot find shopping list by list_id')

        status = ShoppingService.delete_by_id(list_id)
        if not status:
            return render_error('data_does_not_exist', 'failed to delete list')

        return render_response(200, 'ok')

    except Exception as e:
        logging.error(e, exc_info=True)
        return render_error('internal_server_error', "Internal server error")


@shop.route('/api/v1/get_all_lists', methods=['POST'])
def get_all_lists():
    '''
    Get all shopping lists
    '''
    try:
        request_data = request.get_json(force=True)
        if not request_data:
            return render_error('invalid_request', 'request parameters are null')

        limit = request_data.get('limit', None)
        cursor = request_data.get('cursor', None)

        if not isinstance(limit, int) or limit < 0:
            return render_error('invalid_request', 'limit is incorrect')

        if not isinstance(cursor, int) or cursor < 0:
            return render_error('invalid_request', 'cursor is incorrect')

        models, next_page = ShoppingService.get_all_list(limit, cursor)

        data = {
            'shopping_list': models,
            'next_page': next_page,
        }
        if not models:
            return render_response(200, [])

        return render_response(200, data)

    except Exception as e:
        logging.error(e, exc_info=True)
        return render_error('internal_server_error', "Internal server error")


@shop.route('/api/v1/get_lists', methods=['POST'])
def get_lists():
    '''
    Get a shopping list by one or multiple titles or itemId or itemNames
    '''
    try:
        request_data = request.get_json(force=True)
        if not request_data:
            return render_error('invalid_request', 'request parameters are null')

        find_type = request_data.get('findType', None)
        if not find_type:
            return render_error('invalid_request', 'find_type is null')

        title = request_data.get('title', None)
        item_id = request_data.get('itemId', None)
        item_name = request_data.get('itemName', None)

        logging.debug('find_type %s title %s item_id %s item_name %s',
                      find_type, title, item_id, item_name)

        if find_type == 'title':
            if not title:
                return render_error('invalid_request', 'title is null')

            title_list = title.split(',')
            if len(title_list) > 0:
                return render_response(200, pack_custom_response(ShoppingService.get_list_by_title(title_list)))

        elif find_type == 'itemId':
            if not item_id:
                return render_error('invalid_request', 'item_id is null')

            return render_response(200, pack_custom_response(ShoppingService.get_list_by_itemId(item_id)))

        elif find_type == 'itemName':
            if not item_name:
                return render_error('invalid_request', 'item_name is null')

            item_name_list = item_name.split(',')
            if len(item_name_list) > 0:
                return render_response(200, pack_custom_response(ShoppingService.get_list_by_itemname(item_name_list)))

        logging.info('cannot find data find type %s title %s item_id %s item_name %s',
                     find_type, title, item_id, item_name)

        return render_response(200, [])

    except Exception as e:
        logging.error(e, exc_info=True)
        return render_error('internal_server_error', "Internal server error")
