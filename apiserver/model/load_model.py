import logging
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index

db = SQLAlchemy()


class ShoppingList(db.Model):
    __tablename__ = 'shoppinglist'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    shop_name = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return "<ShoppingList(title='%s' shopname='%s')>" % (self.title, self.shop_name)

    @classmethod
    def delete(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return "<Item(Name='%s' Quantity='%s')>" % (self.name, self.quantity)

    @classmethod
    def delete(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()


class ShoppingListItem(db.Model):
    __tablename__ = 'shoppinglistitem'

    id = db.Column(db.Integer, primary_key=True)
    shop_list_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)

    def __repr__(self):
        return "<ShoppingListItem(shop_list_id='%s' item_id='%s')>" % (self.shop_list_id, self.item_id)

    @classmethod
    def delete(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()


def from_sql(row):
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')

    return data


def get_by_list(model, limit=50, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (model.query
             .limit(limit)
             .offset(cursor))

    model = list(map(from_sql, query.all()))
    next_page = cursor + limit if len(model) == limit else None

    return (model, next_page)


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def setup_index(db):
    """
    Create indexes
    """
    item_name_index = Index('item_name', Item.name)
    shop_list_id_indx = Index('shop_list_id', ShoppingListItem.shop_list_id)
    item_id_indx = Index('item_id', ShoppingListItem.item_id)
    title_indx = Index('shop_list_id', ShoppingList.title)

    engine = db.get_engine()

    item_name_index.create(bind=engine)
    shop_list_id_indx.create(bind=engine)
    item_id_indx.create(bind=engine)
    title_indx.create(bind=engine)


def _create_database():
    """
    Create all the tables necessary to run the application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../../settings/config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
        setup_index(db)

    print("All tables created")


if __name__ == '__main__':
    _create_database()
