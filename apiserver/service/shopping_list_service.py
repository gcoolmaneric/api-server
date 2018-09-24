import logging
from sqlalchemy import desc

from apiserver.utils.database_manager import database_manager
from apiserver.model.load_model import ShoppingList


class ShoppingListService(ShoppingList):

    @classmethod
    def create_list(cls, data):
        '''
        Create a shopping list
        '''
        return database_manager.create(data, cls)

    @classmethod
    def read_by_id(cls, id):
        '''
        Query a shopping list by id
        '''
        return database_manager.read_by_id(id, cls)

    @classmethod
    def update_by_id(cls, data, id):
        '''
        Update a shopping list by id and data
        '''
        return database_manager.update_by_id(data, id, cls)

    @classmethod
    def delete_by_id(cls, id):
        '''
        Delete a shopping list by id
        '''
        return database_manager.delete_by_id(id, cls)

    @classmethod
    def get_list(cls, limit=100, cursor=None):
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
        models, next_page = database_manager.get_list(cls, limit, cursor)

        return models, next_page
