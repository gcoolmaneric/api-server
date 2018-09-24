import logging
import re
import json
import pytest

# DEBUG
logging.basicConfig(level=logging.DEBUG)


@pytest.mark.usefixtures('app', 'model', 'item_service')
class TestShopActions(object):

    def test_create_list(self, app):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

    def test_delete_list(self, app):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        data = {
            'listId': response['data']['id']
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/delete_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 'ok' == response['data']

    def test_update_list(self, app):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        list_id = response['data']['id']
        data = {
            'listId': list_id,
            'title': 'testTitle',
            'name': 'testName'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/update_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert list_id == response['data']['id']

    def test_get_all_lists(self, app):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        data = {
            'limit': 1000,
            'cursor': 0,
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/get_all_lists', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert len(response['data']) > 0

    def test_get_all_lists_by_minus_limit(self, app):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        data = {
            'limit': -1,
            'cursor': 0,
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/get_all_lists', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        response = json.loads(rv.data.decode('utf-8'))
        assert 400 == response['status']

    def test_get_all_lists_by_minus_cursor(self, app):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        data = {
            'limit': 100,
            'cursor': -1,
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/get_all_lists', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        response = json.loads(rv.data.decode('utf-8'))
        assert 400 == response['status']

    def test_get_all_lists_by_limit_none_next_page(self, app):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        data = {
            'limit': 1,
            'cursor': 0,
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/get_all_lists', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 1 == len(response['data']['shopping_list'])
        assert 1 == response['data']['next_page']

    def test_get_all_lists_by_limit(self, app):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        data = {
            'limit': 2,
            'cursor': 0,
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/get_all_lists', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 1 == len(response['data']['shopping_list'])
        assert None == response['data']['next_page']

    def test_add_items(self, app, item_service):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        item_service.delete_by_name('banana')
        item_service.delete_by_name('apple')

        data = {
            'listId': response['data']['id'],
            'items': [
                {'name': 'banana', 'quantity': 1},
                {'name': 'apple', 'quantity': 1},
            ]
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/add_items', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 2 == len(response['data']['items'])
        assert 'banana' == response['data']['items'][0]['name']
        assert 1 == int(response['data']['items'][0]['quantity'])
        assert 'apple' == response['data']['items'][1]['name']
        assert 1 == int(response['data']['items'][1]['quantity'])

    def test_add_same_items(self, app, item_service):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        item_service.delete_by_name('tuna')
        item_service.delete_by_name('book')

        # Add items to the shopping list
        data = {
            'listId': response['data']['id'],
            'items': [
                {'name': 'tuna', 'quantity': 1},
                {'name': 'tuna', 'quantity': 5},
                {'name': 'book', 'quantity': 2},
                {'name': 'book', 'quantity': 3},
            ]
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/add_items', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 2 == len(response['data']['items'])
        assert 'tuna' == response['data']['items'][0]['name']
        assert 6 == int(response['data']['items'][0]['quantity'])
        assert 'book' == response['data']['items'][1]['name']
        assert 5 == int(response['data']['items'][1]['quantity'])

    def test_add_exist_mutiple_items(self, app, item_service):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        item_service.delete_by_name('tuna')
        item_service.delete_by_name('book')

        store_id = response['data']['id']

        data = {
            'listId': store_id,
            'items': [
                {'name': 'tuna', 'quantity': 1},
                {'name': 'tuna', 'quantity': 5},
                {'name': 'book', 'quantity': 2},
                {'name': 'book', 'quantity': 3},
            ]
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/add_items', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 2 == len(response['data']['items'])
        assert 'tuna' == response['data']['items'][0]['name']
        assert 6 == int(response['data']['items'][0]['quantity'])
        assert 'book' == response['data']['items'][1]['name']
        assert 5 == int(response['data']['items'][1]['quantity'])

        data = {
            'listId': store_id,
            'items': [
                {'name': 'tuna', 'quantity': 1},
                {'name': 'tuna', 'quantity': 5},
                {'name': 'book', 'quantity': 2},
                {'name': 'book', 'quantity': 3},
            ]
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/add_items', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 2 == len(response['data']['items'])
        assert 'tuna' == response['data']['items'][0]['name']
        assert 12 == int(response['data']['items'][0]['quantity'])
        assert 'book' == response['data']['items'][1]['name']
        assert 10 == int(response['data']['items'][1]['quantity'])

    def test_get_list_by_item_id(self, app, item_service):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        item_service.delete_by_name('banana')
        item_service.delete_by_name('apple')

        # Add items to the shopping list
        data = {
            'listId': response['data']['id'],
            'items': [
                {'name': 'banana', 'quantity': 1},
                {'name': 'apple', 'quantity': 1},
            ]
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/add_items', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 2 == len(response['data']['items'])
        assert 'banana' == response['data']['items'][0]['name']
        assert 1 == int(response['data']['items'][0]['quantity'])
        assert 'apple' == response['data']['items'][1]['name']
        assert 1 == int(response['data']['items'][1]['quantity'])

        data = {
            'findType': 'itemId',
            'title': None,
            'itemId': response['data']['items'][0]['id'],
            'itemName': None,
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/get_lists', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 'banana' == response['data']['items'][0]['name']
        assert 1 == int(response['data']['items'][0]['quantity'])

    def test_get_list_by_item_name(self, app, item_service):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        item_service.delete_by_name('banana')
        item_service.delete_by_name('apple')

        # Add items to the shopping list
        data = {
            'listId': response['data']['id'],
            'items': [
                {'name': 'banana', 'quantity': 1},
                {'name': 'apple', 'quantity': 1},
            ]
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/add_items', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 2 == len(response['data']['items'])
        assert 'banana' == response['data']['items'][0]['name']
        assert 1 == int(response['data']['items'][0]['quantity'])
        assert 'apple' == response['data']['items'][1]['name']
        assert 1 == int(response['data']['items'][1]['quantity'])

        data = {
            'findType': 'itemName',
            'title': None,
            'itemId': None,
            'itemName': response['data']['items'][0]['name'],
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/get_lists', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        logging.debug('get_lists response %s', response)

        assert 200 == response['status']
        assert 'banana' == response['data']['items'][0]['name']
        assert 1 == int(response['data']['items'][0]['quantity'])

    def test_get_list_by_multiple_item_name(self, app, item_service):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        item_service.delete_by_name('banana')
        item_service.delete_by_name('apple')

        # Add items to the shopping list
        data = {
            'listId': response['data']['id'],
            'items': [
                {'name': 'banana', 'quantity': 1},
                {'name': 'apple', 'quantity': 1},
            ]
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/add_items', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 2 == len(response['data']['items'])
        assert 'banana' == response['data']['items'][0]['name']
        assert 1 == int(response['data']['items'][0]['quantity'])
        assert 'apple' == response['data']['items'][1]['name']
        assert 1 == int(response['data']['items'][1]['quantity'])

        data = {
            'findType': 'itemName',
            'title': None,
            'itemId': None,
            'itemName': 'banana, apple',
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/get_lists', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 'banana' == response['data']['items'][0]['name']
        assert 1 == int(response['data']['items'][0]['quantity'])
        assert 'apple' == response['data']['items'][1]['name']
        assert 1 == int(response['data']['items'][1]['quantity'])

    def test_get_list_by_multiple_space_item_name(self, app, item_service):
        data = {
            'title': 'Shopping Title',
            'name': 'Shopping Name'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        item_service.delete_by_name('banana')
        item_service.delete_by_name('apple')

        # Add items to the shopping list
        data = {
            'listId': response['data']['id'],
            'items': [
                {'name': 'banana', 'quantity': 1},
                {'name': 'apple', 'quantity': 1},
            ]
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/add_items', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 2 == len(response['data']['items'])
        assert 'banana' == response['data']['items'][0]['name']
        assert 1 == int(response['data']['items'][0]['quantity'])
        assert 'apple' == response['data']['items'][1]['name']
        assert 1 == int(response['data']['items'][1]['quantity'])

        data = {
            'findType': 'itemName',
            'title': None,
            'itemId': None,
            'itemName': 'banana,             apple',
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/get_lists', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 'banana' == response['data']['items'][0]['name']
        assert 1 == int(response['data']['items'][0]['quantity'])
        assert 'apple' == response['data']['items'][1]['name']
        assert 1 == int(response['data']['items'][1]['quantity'])

    def test_get_list_by_one_title(self, app, item_service):
        data = {
            'title': 'Shopping Title4',
            'name': 'Shopping Name4'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        item_service.delete_by_name('banana')
        item_service.delete_by_name('apple')

        # Add items to the shopping list
        data = {
            'listId': response['data']['id'],
            'items': [
                {'name': 'banana', 'quantity': 1},
                {'name': 'apple', 'quantity': 1},
            ]
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/add_items', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 2 == len(response['data']['items'])
        assert 'banana' == response['data']['items'][0]['name']
        assert 1 == int(response['data']['items'][0]['quantity'])
        assert 'apple' == response['data']['items'][1]['name']
        assert 1 == int(response['data']['items'][1]['quantity'])

        data = {
            'findType': 'title',
            'title': 'Shopping Title4',
            'itemId': None,
            'itemName': None,
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/get_lists', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 'banana' == response['data']['items'][0]['name']
        assert 1 == int(response['data']['items'][0]['quantity'])

    def test_get_list_by_two_titles(self, app, item_service):
        data = {
            'title': 'Shopping Title5',
            'name': 'Shopping Name5'
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/create_list', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert response['data']['id'] > 0

        item_service.delete_by_name('banana')
        item_service.delete_by_name('apple')

        # Add items to the shopping list
        data = {
            'listId': response['data']['id'],
            'items': [
                {'name': 'banana', 'quantity': 1},
                {'name': 'apple', 'quantity': 1},
            ]
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/add_items', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 2 == len(response['data']['items'])
        assert 'banana' == response['data']['items'][0]['name']
        assert int(response['data']['items'][0]['quantity']) == 1
        assert 'apple' == response['data']['items'][1]['name']
        assert int(response['data']['items'][1]['quantity']) == 1

        data = {
            'findType': 'title',
            'title': 'Shopping Title4,Shopping Title5',
            'itemId': None,
            'itemName': None,
        }

        with app.test_client() as c:
            rv = c.post('/shop/api/v1/get_lists', data=json.dumps(data),
                        follow_redirects=True, content_type='application/json')

        assert rv.status == '200 OK'
        response = json.loads(rv.data.decode('utf-8'))

        assert 200 == response['status']
        assert 'banana' == response['data']['items'][0]['name']
        assert int(response['data']['items'][0]['quantity']) == 1
