import logging
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

logging.basicConfig(level=logging.DEBUG)


class Singleton(object):
    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
        return class_._instances[class_]


class DatabaseManager(Singleton):
    _db = None

    def __init__(self):
        if not self._db:
            self._db = SQLAlchemy()

    def get_db(self):
        return self._db

    def from_sql(self, row):
        '''
        Serialize data from database to proper dictionary
        '''
        data = row.__dict__.copy()
        data['id'] = row.id
        data.pop('_sa_instance_state')

        return data

    def get_list(self, model, limit=50, cursor=None):
        '''
        Query all model's data in a list by limit and cursor.
        This allow you query big data for different models by paging.

        Input:
        limit: the maximum number of data to be retrieved (integer)
        cursor: an index of begining position to query (integer)

        Return:
        result_model: retrieved data
        next_page: current position

        If cursor + limit > maximum number of rows, next_page will return None
        '''
        cursor = int(cursor) if cursor else 0
        query = (model.query
                 .order_by(desc(model.id))
                 .limit(limit)
                 .offset(cursor))

        result_model = list(map(self.from_sql, query.all()))
        next_page = cursor + limit if len(result_model) == limit else None

        return (result_model, next_page)

    def read_by_id(self, id, model):
        '''
        Query mode by id
        '''
        result = model.query.get(id)
        if not result:
            return None

        return self.from_sql(result)

    def create(self, data, model):
        '''
        Create data for model
        '''
        _model = model(**data)
        self._db.session.add(_model)
        self._db.session.commit()

        return self.from_sql(_model)

    def update_by_id(self, data, id, model):
        '''
        Update model's data by id
        '''
        _model = self._db.session.query(model).get(id)
        for k, v in data.items():
            setattr(_model, k, v)

        self._db.session.commit()

        return self.from_sql(_model)

    def delete_by_id(self, id, model):
        '''
        Delete model's data by id
        '''
        rows_deleted = self._db.session.query(model).filter_by(id=id).delete()
        self._db.session.commit()

        if int(rows_deleted) > 0:
            return True

        return False


# Initial Dababase Mamager instance and db
database_manager = DatabaseManager()
db = database_manager.get_db()
