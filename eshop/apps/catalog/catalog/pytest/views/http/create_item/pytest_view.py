from typing import cast

import fastapi
from fastapi import HTTPException, status

from mock import Mock, patch

import pytest

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from catalog.app_config import CatalogAppConfig
from catalog.domain.models.catalog_item import CatalogItem
from catalog.views.http.create_item import create_item
from catalog.views.http.create_item.view import NewCatalogItemRequestData

from eshop.dependency_container import dependency_container

from framework.file_storage.ifile_storage_api import IFileStorageApi, UploadFile
from framework.for_pytests.file_storage.mock_type import FileStorageApiMockType
from framework.for_pytests.for_testing_http_views import ExpectedHttpResponse
from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass


class TestSuccessCase(TestCase['TestCreateItemView']):
    new_catalog_item_request_data: NewCatalogItemRequestData
    catalog_item_picture: fastapi.UploadFile
    expected_http_response: ExpectedHttpResponse
    file_storage_api_mock: FileStorageApiMockType
    expected_created_catalog_item: CatalogItem


class TestFailedDueToIntegrityErrorCase(TestCase['TestCreateItemView']):
    new_catalog_item_request_data: NewCatalogItemRequestData
    catalog_item_picture: fastapi.UploadFile
    expected_http_exception_status_code: int
    file_storage_api_mock: FileStorageApiMockType


@pytest.fixture(scope='session')
def test_success_case() -> TestSuccessCase:
    new_catalog_item_request_data = NewCatalogItemRequestData(
        name='name',
        description='description',
        price=10,
        catalog_type_id=1,
        catalog_brand_id=1,
        available_stock=10,
        restock_threshold=15,
        maxstock_threshold=20,
        on_reorder=True,
        discount=50,
    )

    catalog_item_picture = fastapi.UploadFile(file=Mock(), filename='picture.jpeg')

    file_storage_api_mock = Mock(spec=IFileStorageApi)
    file_storage_api_mock.url_path_for_file.return_value = 'picture_url'
    file_storage_api_mock.upload.return_value = None

    expected_created_catalog_item = CatalogItem(
        name='name',
        description='description',
        price=10,
        picture_filename='picture.jpeg',
        picture_url='picture_url',
        catalog_type_id=1,
        catalog_brand_id=1,
        available_stock=10,
        restock_threshold=15,
        maxstock_threshold=20,
        on_reorder=True,
        discount=50,
    )

    return TestSuccessCase(
        new_catalog_item_request_data=new_catalog_item_request_data,
        expected_created_catalog_item=expected_created_catalog_item,
        catalog_item_picture=catalog_item_picture,
        expected_http_response=ExpectedHttpResponse(
            status_code=status.HTTP_201_CREATED,
            body=b'',
        ),
        file_storage_api_mock=file_storage_api_mock,
    )


@pytest.fixture(scope='session')
def test_failed_due_to_integrity_error_case() -> TestFailedDueToIntegrityErrorCase:
    new_catalog_item_request_data = NewCatalogItemRequestData(
        name='name',
        description='description',
        price=10,
        picture_filename='picture_filename',
        picture_url='picture_url',
        catalog_type_id=1,
        catalog_brand_id=1,
        available_stock=10,
        restock_threshold=15,
        maxstock_threshold=20,
        on_reorder=True,
        discount=50,
    )

    catalog_item_picture = fastapi.UploadFile(file=Mock(), filename='picture.jpeg')

    file_storage_api_mock = Mock(spec=IFileStorageApi)
    file_storage_api_mock.url_path_for_file.return_value = 'picture_url'
    file_storage_api_mock.upload.return_value = None

    return TestFailedDueToIntegrityErrorCase(
        new_catalog_item_request_data=new_catalog_item_request_data,
        catalog_item_picture=catalog_item_picture,
        expected_http_exception_status_code=status.HTTP_400_BAD_REQUEST,
        file_storage_api_mock=file_storage_api_mock,
    )


class TestUrlToView(TestClass[create_item]):
    def test(self):
        expected_url = '/catalog/items/'
        fact_url = CatalogAppConfig.get_api_router().url_path_for(create_item.__name__)
        assert fact_url == expected_url


class TestCreateItemView(TestClass[create_item]):
    @staticmethod
    def _assert_catalog_item(fact: CatalogItem, expected: CatalogItem) -> None:
        assert fact.name == expected.name
        assert fact.description == expected.description
        assert fact.price == expected.price
        assert fact.picture_filename == expected.picture_filename
        assert fact.picture_url == expected.picture_url
        assert fact.catalog_type_id == expected.catalog_type_id
        assert fact.catalog_brand_id == expected.catalog_brand_id
        assert fact.available_stock == expected.available_stock
        assert fact.restock_threshold == expected.restock_threshold
        assert fact.maxstock_threshold == expected.maxstock_threshold
        assert fact.on_reorder == expected.on_reorder
        assert fact.discount == expected.discount

    @patch.object(Session, Session.add.__name__)
    def test_success_case(
        self,
        mock__session__add: Mock,
        test_success_case: TestSuccessCase,
    ):
        test_case = test_success_case

        mock__session__add.return_value = None

        with dependency_container.file_storage_api_factory.override(test_case.file_storage_api_mock):
            response = create_item(
                new_catalog_item_request_data=test_case.new_catalog_item_request_data,
                catalog_item_picture=test_case.catalog_item_picture,
            )

        assert response.status_code == test_case.expected_http_response.status_code
        assert response.body == test_case.expected_http_response.body

        cast(Mock, test_case.file_storage_api_mock.url_path_for_file) \
            .assert_called_once_with(filename=test_case.catalog_item_picture.filename)

        fact_created_catalog_item: CatalogItem = mock__session__add.call_args_list[0].args[0]

        self._assert_catalog_item(
            fact=fact_created_catalog_item,
            expected=test_case.expected_created_catalog_item,
        )

        cast(Mock, test_case.file_storage_api_mock.upload) \
            .assert_called_once_with(
                upload_file=UploadFile(
                    file=test_case.catalog_item_picture.file,
                    filename=test_case.catalog_item_picture.filename,
                ),
            )

    @patch.object(Session, Session.flush.__name__)
    def test_failed_due_to_integrity_error_case(
        self,
        mock__session__flush: Mock,
        test_failed_due_to_integrity_error_case: TestFailedDueToIntegrityErrorCase,
    ):
        test_case = test_failed_due_to_integrity_error_case

        mock__session__flush.side_effect = IntegrityError(orig=None, statement=None, params=None)

        with dependency_container.file_storage_api_factory.override(test_case.file_storage_api_mock):
            try:
                create_item(
                    new_catalog_item_request_data=test_case.new_catalog_item_request_data,
                    catalog_item_picture=test_case.catalog_item_picture,
                )
            except HTTPException as e:
                assert e.status_code == test_case.expected_http_exception_status_code

        cast(Mock, test_case.file_storage_api_mock.url_path_for_file) \
            .assert_called_once_with(filename=test_case.catalog_item_picture.filename)

        cast(Mock, test_case.file_storage_api_mock.upload) \
            .assert_not_called()
