import logging

from apiserver.utils.database_manager import database_manager
from apiserver.model.load_model import ShoppingListItem


class ShoppingListItemService(ShoppingListItem):
    @classmethod
    def check_or_create(cls, list_id, item):
        '''
        Check or create ShoppingListItem data
        '''
        query = (ShoppingListItem.query
                 .filter_by(shop_list_id=list_id, item_id=item.get('id'))
                 .one_or_none())

        if not query:
            database_manager.create({
                'shop_list_id': list_id,
                'item_id': item.get('id')
            }, cls)
