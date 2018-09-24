import logging

from flask import current_app, Flask, redirect, url_for


def create_app(config, debug=True, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        model = get_model()
        model.init_app(app)

    # Initial api
    from apiserver.api.shop import shop

    app.register_blueprint(shop, url_prefix='/shop')

    # Add an error handler
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app


def get_model():
    from apiserver.model import load_model
    model = load_model

    return model


def get_item_service():
    from apiserver.service.item_service import ItemService
    service = ItemService

    return service


def shopping_service():
    from apiserver.service.shopping_service import ShoppingService
    service = ShoppingService

    return service


def get_shopping_list_service():
    from apiserver.service.shopping_list_service import ShoppingListService
    service = ShoppingListService

    return service


def get_shopping_service():
    from apiserver.service.shopping_service import ShoppingService
    service = ShoppingService

    return service


def get_shopping_list_item_service():
    from apiserver.service.shopping_list_item_service import ShoppingListItemService
    service = ShoppingListItemService

    return service
