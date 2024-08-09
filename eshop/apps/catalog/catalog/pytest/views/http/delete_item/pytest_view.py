from typing import cast

from fastapi import status

from mock import Mock, patch

import pytest

from catalog import hints
from catalog.app_config import CatalogAppConfig
from catalog.views.http.delete_item import delete_item, view

from catalog_cqrs_contract.event import CatalogItemHasBeenDeletedEvent

from eshop.dependency_container import dependency_container

from framework.cqrs.context import InsideSqlachemyTransactionContext
from framework.file_storage import IFileStorageApi
from framework.for_pytests.file_storage.mock_type import FileStorageApiMockType
from framework.for_pytests.for_testing_http_views import ExpectedHttpResponse
from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass
from framework.sqlalchemy.session import Session


class TestCaseCatalogItemExists(TestCase['TestDeleteItemView']):
    catalog_item_id: hints.CatalogItemId
    mock__fetch_catalog_item_picture_url__return_value: str
    expected_published_event: CatalogItemHasBeenDeletedEvent
    expected_response: ExpectedHttpResponse
    mock__file_storage_api: FileStorageApiMockType


class TestCaseCatalogItemDoesNotExist(TestCase['TestDeleteItemView']):
    catalog_item_id: hints.CatalogItemId
    expected_response: ExpectedHttpResponse


@pytest.fixture(scope='session')
def test_case_catalog_item_exists() -> TestCaseCatalogItemExists:
    catalog_item_id = 1

    expected_published_event = CatalogItemHasBeenDeletedEvent(
        catalog_item_id=catalog_item_id,
        context=InsideSqlachemyTransactionContext(session=Session()),
    )

    mock__fetch_catalog_item_picture_url__return_value = 'picture_url'

    mock__file_storage_api = Mock(spec=IFileStorageApi)
    mock__file_storage_api.delete.return_value = None

    return TestCaseCatalogItemExists(
        catalog_item_id=catalog_item_id,
        expected_published_event=expected_published_event,
        expected_response=ExpectedHttpResponse(
            status_code=status.HTTP_200_OK,
            body=b'',
        ),
        mock__fetch_catalog_item_picture_url__return_value=mock__fetch_catalog_item_picture_url__return_value,
        mock__file_storage_api=mock__file_storage_api,
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
    @patch.object(CatalogItemHasBeenDeletedEvent, 'publish', autospec=True)
    @patch.object(view, '_fetch_catalog_item_picture_url')
    @patch.object(view, '_delete_catalog_item_from_db')
    @patch.object(view, '_check_if_catalog_item_exists')
    def test_case_catalog_item_exists(
        self,
        mock__check_if_catalog_item_exists: Mock,
        mock__delete_catalog_item_from_db: Mock,
        mock__fetch_catalog_item_picture_url: Mock,
        mock__catalog_item_has_been_deleted_event__publish: Mock,
        test_case_catalog_item_exists: TestCaseCatalogItemExists,
    ):
        test_case = test_case_catalog_item_exists

        mock__check_if_catalog_item_exists.return_value = True

        mock__delete_catalog_item_from_db.return_value = None

        mock__fetch_catalog_item_picture_url.return_value = (
            test_case.mock__fetch_catalog_item_picture_url__return_value
        )

        mock__catalog_item_has_been_deleted_event__publish.return_value = None

        with dependency_container.file_storage_api_factory.override(test_case.mock__file_storage_api):
            response = delete_item(catalog_item_id=test_case.catalog_item_id)

        assert response.status_code == test_case.expected_response.status_code
        assert response.body == test_case.expected_response.body

        mock__catalog_item_has_been_deleted_event__publish.assert_called_once()
        fact_published_event: CatalogItemHasBeenDeletedEvent = (
            mock__catalog_item_has_been_deleted_event__publish.call_args[0][0]
        )
        assert fact_published_event == test_case.expected_published_event

        cast(Mock, test_case.mock__file_storage_api.delete).assert_called_once_with(
            url_path_to_file=test_case.mock__fetch_catalog_item_picture_url__return_value,
        )

    @patch.object(CatalogItemHasBeenDeletedEvent, 'publish')
    @patch.object(view, '_check_if_catalog_item_exists')
    def test_case_catalog_item_does_not_exist(
        self,
        mock__check_if_catalog_item_exists: Mock,
        mock__catalog_item_has_been_deleted_event__publish: Mock,
        test_case_catalog_item_does_not_exist: TestCaseCatalogItemDoesNotExist,
    ):
        test_case = test_case_catalog_item_does_not_exist

        mock__check_if_catalog_item_exists.return_value = False

        response = delete_item(catalog_item_id=test_case.catalog_item_id)
        assert response.status_code == test_case.expected_response.status_code
        assert response.body == test_case.expected_response.body

        mock__catalog_item_has_been_deleted_event__publish.assert_not_called()
