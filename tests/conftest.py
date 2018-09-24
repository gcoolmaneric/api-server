"""conftest.py is used to define common test fixtures for pytest."""
import logging
import pytest
import apiserver
import settings

from settings import config
from retrying import retry

# DEBUG
logging.basicConfig(level=logging.DEBUG)


@pytest.yield_fixture(params=['cloudsql'])
def app(request):
    app = apiserver.create_app(
        config,
        testing=True,
        config_overrides={
            'DATA_BACKEND': request.param
        })

    with app.test_request_context():
        yield app


@pytest.yield_fixture
def item_service(monkeypatch, app):

    service = apiserver.get_item_service()

    yield service


@pytest.yield_fixture
def shopping_list_service(monkeypatch, app):
    service = apiserver.get_shopping_list_service()

    yield service


@pytest.yield_fixture
def shopping_service(monkeypatch, app):
    service = apiserver.get_shopping_service()

    yield service


@pytest.yield_fixture
def shopping_list_item_service(monkeypatch, app):
    service = apiserver.shopping_list_item_service()

    yield service


@pytest.yield_fixture
def model(monkeypatch, app):
    model = apiserver.get_model()

    yield model

    # Delete all models that we created during tests.
    delete_all_model(model.Item, model.get_by_list)
    delete_all_model(model.ShoppingList, model.get_by_list)
    delete_all_model(model.ShoppingListItem, model.get_by_list)


@retry(
    stop_max_attempt_number=3,
    wait_exponential_multiplier=100,
    wait_exponential_max=2000)
def delete_all_model(model, model_list):
    while True:
        models, _ = model_list(model, limit=50)
        if not models:
            break
        for data in models:
            model.delete(data['id'])
