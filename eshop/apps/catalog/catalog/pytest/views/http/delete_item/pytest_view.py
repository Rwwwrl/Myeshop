from fastapi import status

from mock import Mock, patch

import pytest

from catalog import hints
from catalog.app_config import CatalogAppConfig
from catalog.views.http.delete_item import delete_item, view

from catalog_cqrs_contract.event import CatalogItemHasBeenDeletedEvent

from framework.cqrs.context import InsideSqlachemySessionContext
from framework.cqrs.cqrs_bus import CQRSBus
from framework.for_pytests.for_testing_http_views import ExpectedHttpResponse
from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass
from framework.sqlalchemy.session import Session


class TestCaseCatalogItemExists(TestCase['TestDeleteItemView']):
    catalog_item_id: hints.CatalogItemId
    expected_published_event: CatalogItemHasBeenDeletedEvent
    expected_response: ExpectedHttpResponse


class TestCaseCatalogItemDoesNotExist(TestCase['TestDeleteItemView']):
    catalog_item_id: hints.CatalogItemId
    expected_response: ExpectedHttpResponse


@pytest.fixture(scope='session')
def test_case_catalog_item_exists() -> TestCaseCatalogItemExists:
    catalog_item_id = 1
    expected_published_event = CatalogItemHasBeenDeletedEvent(
        catalog_item_id=catalog_item_id,
        context=InsideSqlachemySessionContext(session=Session()),
    )
    return TestCaseCatalogItemExists(
        catalog_item_id=catalog_item_id,
        expected_published_event=expected_published_event,
        expected_response=ExpectedHttpResponse(
            status_code=status.HTTP_200_OK,
            body=b'',
        ),
    )


@pytest.fixture(scope='session')
def test_case_catalog_item_does_not_exist() -> TestCaseCatalogItemDoesNotExist:
    catalog_item_id = 1
    return TestCaseCatalogItemDoesNotExist(
        catalog_item_id=catalog_item_id,
        expected_response=ExpectedHttpResponse(
            status_code=status.HTTP_200_OK,
            body=b'',
        ),
    )


class TestUrlToView(TestClass[delete_item]):
    def test(self):
        expected_url = '/catalog/items/'
        fact_url = CatalogAppConfig.get_api_router().url_path_for(delete_item.__name__)
        assert fact_url == expected_url


class TestDeleteItemView(TestClass[delete_item]):
    @patch.object(CQRSBus, 'publish')
    @patch.object(view, '_delete_catalog_item_from_db')
    @patch.object(view, '_check_if_catalog_item_exists')
    def test_case_catalog_item_exists(
        self,
        mock__check_if_catalog_item_exists: Mock,
        mock__delete_catalog_item_from_db: Mock,
        mock__cqrsbus__publish: Mock,
        test_case_catalog_item_exists: TestCaseCatalogItemExists,
    ):
        test_case = test_case_catalog_item_exists

        mock__check_if_catalog_item_exists.return_value = True

        mock__delete_catalog_item_from_db.return_value = None

        mock__cqrsbus__publish.return_value = None

        response = delete_item(catalog_item_id=test_case.catalog_item_id)
        assert response.status_code == test_case.expected_response.status_code
        assert response.body == test_case.expected_response.body

        mock__cqrsbus__publish.assert_called_once_with(event=test_case.expected_published_event)

    @patch.object(CQRSBus, 'publish')
    @patch.object(view, '_check_if_catalog_item_exists')
    def test_case_catalog_item_does_not_exist(
        self,
        mock__check_if_catalog_item_exists: Mock,
        mock__cqrsbus__publish: Mock,
        test_case_catalog_item_does_not_exist: TestCaseCatalogItemDoesNotExist,
    ):
        test_case = test_case_catalog_item_does_not_exist

        mock__check_if_catalog_item_exists.return_value = False

        response = delete_item(catalog_item_id=test_case.catalog_item_id)
        assert response.status_code == test_case.expected_response.status_code
        assert response.body == test_case.expected_response.body

        mock__cqrsbus__publish.assert_not_called()
