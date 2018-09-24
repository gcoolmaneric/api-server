import logging
import re
import json
import pytest

# DEBUG
logging.basicConfig(level=logging.DEBUG)


@pytest.mark.usefixtures('app', 'model', 'shopping_list_service')
class TestShoppingListService(object):

    def test_create_list(self, shopping_list_service):
        data = shopping_list_service.create_list({
            'title': 'test-title1',
            'shop_name': 'test-name1',
        })

        assert data['id'] > 0

    def test_read_by_id(self, shopping_list_service):
        data = shopping_list_service.create_list({
            'title': 'test-title2',
            'shop_name': 'test-name2',
        })

        assert data['id'] > 0

        data = shopping_list_service.read_by_id(data['id'])

        assert data['title'] == 'test-title2'
        assert data['shop_name'] == 'test-name2'

    def test_update_by_id(self, shopping_list_service):
        data = shopping_list_service.create_list({
            'title': 'test-title2',
            'shop_name': 'test-name2',
        })

        assert data['id'] > 0

        updated_data = shopping_list_service.update_by_id({
            'title': 'test-title33',
            'shop_name': 'test-name33',
        }, data['id'])

        assert updated_data['id'] == data['id']

    def test_delete_by_id(self, shopping_list_service):
        data = shopping_list_service.create_list({
            'title': 'test-title22',
            'shop_name': 'test-name22',
        })

        assert data['id'] > 0

        store_id = data['id']

        data = shopping_list_service.delete_by_id(store_id)

        assert data == True

        data = shopping_list_service.read_by_id(store_id)
        assert data == None

    def test_get_list(self, shopping_list_service):
        data = shopping_list_service.create_list({
            'title': 'test-title1',
            'shop_name': 'test-name1',
        })
        assert data['id'] > 0

        data = shopping_list_service.create_list({
            'title': 'test-title2',
            'shop_name': 'test-name2',
        })
        assert data['id'] > 0

        data = shopping_list_service.create_list({
            'title': 'test-title3',
            'shop_name': 'test-name3',
        })
        assert data['id'] > 0

        models, next_page = shopping_list_service.get_list()

        assert len(models) >= 3

    def test_get_list_by_limit(self, shopping_list_service):
        data = shopping_list_service.create_list({
            'title': 'test-title1',
            'shop_name': 'test-name1',
        })
        assert data['id'] > 0

        data = shopping_list_service.create_list({
            'title': 'test-title2',
            'shop_name': 'test-name2',
        })
        assert data['id'] > 0

        data = shopping_list_service.create_list({
            'title': 'test-title3',
            'shop_name': 'test-name3',
        })
        assert data['id'] > 0

        data = shopping_list_service.create_list({
            'title': 'test-title4',
            'shop_name': 'test-name4',
        })
        assert data['id'] > 0

        models, next_page = shopping_list_service.get_list(limit=100, cursor=2)

        assert len(models) >= 0
