import logging
from sqlalchemy import text
from apiserver.utils.database_manager import database_manager, db

from apiserver.model.load_model import ShoppingList, ShoppingListItem, Item
from apiserver.service.item_service import ItemService
from apiserver.service.shopping_list_item_service import ShoppingListItemService
from apiserver.service.shopping_list_service import ShoppingListService

# DEBUG
logging.basicConfig(level=logging.DEBUG)


class ShoppingService(object):

    def __init__(self):
        pass

    @classmethod
    def create_list(cls, title, name):
        '''
        Create a shoppinglist
        '''
        return ShoppingListService.create_list({
            'title': title,
            'shop_name': name,
        })

    @classmethod
    def add_items(cls, shop_list_id, items):
        '''
        Add or update itmes by ItemService; update its relationship by ShoppingListItemService
        '''
        if not items:
            return None

        item_dict = {}
        for data in items:
            if not data or not data.get('name') or not data.get('quantity'):
                logging.error('invalid items data %s', data)
                continue

            if data['name'] not in item_dict:
                item_dict[data['name']] = data
            else:
                item = item_dict.get(data['name'])
                item['quantity'] += data['quantity']
                item_dict[data['name']] = item

        item_list = []
        for key, data in item_dict.items():
            item_data = ItemService.create_or_update(data)
            if item_data:
                ShoppingListItemService.check_or_create(shop_list_id, item_data)
                item_list.append(item_data)

        return item_list

    @classmethod
    def get_shop_by_list_id(cls, shop_list_id):
        '''
        Get a shoppinglist by shop_list_id
        '''
        if not shop_list_id:
            return

        return ShoppingListService.read_by_id(shop_list_id)

    @classmethod
    def get_list_by_shop_list_id(cls, shop_list_id):
        '''
        Query ShoppingList with shop_list_id by joining ShoppingList,
        ShoppingListItem and Item tables
        '''
        if not shop_list_id:
            return

        result = (db.session.query(ShoppingList, ShoppingListItem, Item)
                  .filter(ShoppingList.id == shop_list_id)
                  .filter(ShoppingListItem.shop_list_id == ShoppingList.id)
                  .filter(ShoppingListItem.item_id == Item.id)
                  .all())

        response_data = []
        for row in result:
            model = list(map(database_manager.from_sql, row))
            response_data.extend(model)

        if not response_data:
            logging.error('failed to add items shop_list_id %s', shop_list_id)
            return

        return response_data

    @classmethod
    def update_list(cls, data, shop_list_id):
        '''
        Update a shoppinglist by shop_list_id
        '''
        return ShoppingListService.update_by_id(data, shop_list_id)

    @classmethod
    def delete_by_id(cls, shop_list_id):
        '''
        Delete a shoppinglist by shop_list_id
        '''
        return ShoppingListService.delete_by_id(shop_list_id)

    @classmethod
    def get_all_list(cls, limit, cursor):
        '''
        Get all shoppinglists by limit and cursor.
        This allow you query big data for ShoppingList table by paging.

        Input:
        limit: the maximum number of data to be retrieved (integer)
        cursor: an index of begining position to query (integer)

        Return:
        model: retrieved data
        next_page: current position

        If cursor + limit > maximum number of rows, next_page will return None
        '''
        return ShoppingListService.get_list(limit, cursor)

    @classmethod
    def get_list_by_title(cls, titles):
        '''
        Query ShoppingList with multuple titles by joining ShoppingList,
        ShoppingListItem and Item tables
        '''
        response_data = []

        for title in titles:
            if not title:
                continue

            result = (db.session.query(Item, ShoppingListItem, ShoppingList)
                      .filter(ShoppingList.title.like(title.strip()))
                      .filter(ShoppingListItem.item_id == Item.id)
                      .filter(ShoppingList.id == ShoppingListItem.shop_list_id)
                      .all())

            for row in result:
                model = list(map(database_manager.from_sql, row))
                response_data.extend(model)

            if not response_data:
                logging.error('failed to get_list_by_title title %s', title)
                continue

        return response_data

    @classmethod
    def get_list_by_itemId(cls, itemid):
        '''
        Query ShoppingList with itemId by joining ShoppingList,
        ShoppingListItem and Item tables
        '''
        result = (db.session.query(Item, ShoppingListItem, ShoppingList)
                  .filter(Item.id == itemid)
                  .filter(ShoppingListItem.item_id == Item.id)
                  .filter(ShoppingList.id == ShoppingListItem.shop_list_id)
                  .all())

        response_data = []
        for row in result:
            model = list(map(database_manager.from_sql, row))
            response_data.extend(model)

        if not response_data:
            logging.error('failed to get_list_by_itemId itemid %s', itemid)
            return

        return response_data

    @classmethod
    def get_list_by_itemname(cls, item_names):
        '''
        Query ShoppingList with multiple item names by joining ShoppingList,
        ShoppingListItem and Item tables
        '''
        response_data = []

        for name in item_names:
            if not name:
                continue

            result = (db.session.query(ShoppingList, ShoppingListItem, Item)
                      .filter(Item.name.like(name.strip()))
                      .filter(ShoppingListItem.shop_list_id == ShoppingList.id)
                      .filter(ShoppingListItem.item_id == Item.id)
                      .all())

            for row in result:
                model = list(map(database_manager.from_sql, row))
                response_data.extend(model)

            if not response_data:
                logging.error('failed to get_list_by_itemId item name %s', name)
                continue

        return response_data
