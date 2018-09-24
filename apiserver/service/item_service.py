import logging
from sqlalchemy import desc

from apiserver.utils.database_manager import database_manager, db
from apiserver.model.load_model import Item


class ItemService(Item):
    @classmethod
    def create_item(cls, item):
        '''
        Create item
        '''
        return database_manager.create(item, cls)

    @classmethod
    def delete_item(cls, id):
        '''
        Delete item by id
        '''
        return database_manager.delete_by_id(id, cls)

    @classmethod
    def delete_by_name(cls, name):
        '''
        Delete item by item name
        '''
        query = (db.session.query(Item)
                 .filter(Item.name == name)
                 .order_by(desc(Item.id))
                 .limit(1)
                 .offset(None))

        result_model = list(map(database_manager.from_sql, query.all()))
        if result_model and len(result_model) > 0:
            data = result_model[0]
            item_data = database_manager.delete_by_id(data['id'], cls)

    @classmethod
    def create_or_update(cls, item):
        '''
        Create item or update item's quantity
        '''
        query = (db.session.query(Item)
                 .filter(Item.name == item.get('name'))
                 .order_by(desc(Item.id))
                 .limit(1)
                 .offset(None))

        result_model = list(map(database_manager.from_sql, query.all()))
        if not result_model or len(result_model) == 0:
            item_data = database_manager.create(item, Item)
        else:
            data = result_model[0]
            data['quantity'] = int(item['quantity']) + int(data['quantity'])
            item_data = database_manager.update_by_id(data, data['id'], cls)

        return item_data
