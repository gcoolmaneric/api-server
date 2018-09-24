import logging
import re
import json
import pytest


@pytest.mark.usefixtures('app', 'model', 'item_service')
class TestItemService(object):

    def test_create_item(self, item_service):
        data = item_service.create_item({
            'name': 'item1',
            'quantity': 1,
        })

        assert data['id'] > 0

    def test_delete_item(self, item_service):
        data = item_service.create_item({
            'name': 'item1',
            'quantity': 1,
        })

        assert data['id'] > 0

        data = item_service.delete_item(data['id'])

        assert data == True

    def test_check_or_update_item(self, item_service):
        data = item_service.create_item({
            'name': 'item1',
            'quantity': 1,
        })

        assert data['id'] > 0

        data = item_service.create_or_update({
            'name': 'item1',
            'quantity': 2,
        })

        assert data['id'] > 0
