from typing import cast

import fastapi
from fastapi import HTTPException, status

from mock import Mock, patch

import pytest

from sqlalchemy.exc import IntegrityError

from catalog.app_config import CatalogAppConfig
from catalog.views.http.update_item import update_item, view
from catalog.views.http.update_item.view import (
    CatalogItemPriceAndPictureFilenameResult,
    CatalogItemRequestData,
    NotFoundError,
)

from catalog_cqrs_contract.event import CatalogItemPriceChangedEvent

from eshop.dependency_container import dependency_container

from framework.cqrs.context import InsideSqlachemyTransactionContext
from framework.file_storage import IFileStorageApi, UploadFile
from framework.for_pytests.file_storage.mock_type import FileStorageApiMockType
from framework.for_pytests.for_testing_http_views import ExpectedHttpResponse
from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass
from framework.sqlalchemy.session import Session


class TestCaseSuccessButPriceWasNotChanged(TestCase['TestUpdateItemView']):
    mock__fetch_catalog_item_price_and_picture_filename__return_value: CatalogItemPriceAndPictureFilenameResult
    catalog_item_request_data: CatalogItemRequestData
    catalog_item_picture: fastapi.UploadFile
    expected_response: ExpectedHttpResponse
    mock__file_storage_api: FileStorageApiMockType


class TestCaseSuccessButPriceHasBeenChanged(TestCase['TestUpdateItemView']):
    mock__fetch_catalog_item_price_and_picture_filename__return_value: CatalogItemPriceAndPictureFilenameResult
    catalog_item_request_data: CatalogItemRequestData
    catalog_item_picture: fastapi.UploadFile
    expected_published_event: CatalogItemPriceChangedEvent
    expected_response: ExpectedHttpResponse
    mock__file_storage_api: FileStorageApiMockType


class TestCaseFailedDueToIntegrityError(TestCase['TestUpdateItemView']):
    mock__fetch_catalog_item_price_and_picture_filename__return_value: CatalogItemPriceAndPictureFilenameResult
    catalog_item_request_data: CatalogItemRequestData
    catalog_item_picture: fastapi.UploadFile


class TestCaseFailedDueToNotFoundError(TestCase['TestUpdateItemView']):
    catalog_item_request_data: CatalogItemRequestData
    catalog_item_picture: fastapi.UploadFile


@pytest.fixture(scope='session')
def test_case_sucess_but_price_was_not_changed() -> TestCaseSuccessButPriceWasNotChanged:
    mock__fetch_catalog_item_price_and_picture_filename__return_value = CatalogItemPriceAndPictureFilenameResult(
        price=10,
        picture_filename='picture_filename',
    )

    catalog_item_request_data = CatalogItemRequestData(
        id=1,
        name='name',
        description='description',
        price=mock__fetch_catalog_item_price_and_picture_filename__return_value.price,
        picture_filename='new_picture_filename',
        picture_url='picture_url',
        catalog_type_id=1,
        catalog_brand_id=2,
        available_stock=10,
        restock_threshold=15,
        maxstock_threshold=20,
        on_reorder=False,
    )

    catalog_item_picture = fastapi.UploadFile(file=Mock(), filename='picture.jpeg')

    mock__file_storage_api = Mock(spec=IFileStorageApi)
    mock__file_storage_api.update.return_value = None

    return TestCaseSuccessButPriceWasNotChanged(
        catalog_item_request_data=catalog_item_request_data,
        catalog_item_picture=catalog_item_picture,
        mock__fetch_catalog_item_price_and_picture_filename__return_value=(
            mock__fetch_catalog_item_price_and_picture_filename__return_value
        ),
        expected_response=ExpectedHttpResponse(
            status_code=status.HTTP_200_OK,
            body=b'',
        ),
        mock__file_storage_api=mock__file_storage_api,
    )


@pytest.fixture(scope='session')
def test_case_success_but_price_has_been_changed() -> TestCaseSuccessButPriceHasBeenChanged:
    mock__fetch_catalog_item_price_and_picture_filename__return_value = CatalogItemPriceAndPictureFilenameResult(
        price=10,
        picture_filename='picture_filename',
    )

    catalog_item_request_data = CatalogItemRequestData(
        id=1,
        name='name',
        description='description',
        price=15,
        picture_filename='picture_filename',
        picture_url='picture_filename',
        catalog_type_id=1,
        catalog_brand_id=2,
        available_stock=10,
        restock_threshold=15,
        maxstock_threshold=20,
        on_reorder=False,
    )

    catalog_item_picture = fastapi.UploadFile(file=Mock(), filename='picture.jpeg')

    mock__file_storage_api = Mock(spec=IFileStorageApi)
    mock__file_storage_api.update.return_value = None

    expected_published_event = CatalogItemPriceChangedEvent(
        catalog_item_id=1,
        old_price=10,
        new_price=15,
        context=InsideSqlachemyTransactionContext(session=Session()),
    )

    return TestCaseSuccessButPriceHasBeenChanged(
        catalog_item_request_data=catalog_item_request_data,
        catalog_item_picture=catalog_item_picture,
        mock__fetch_catalog_item_price_and_picture_filename__return_value=(
            mock__fetch_catalog_item_price_and_picture_filename__return_value
        ),
        expected_published_event=expected_published_event,
        expected_response=ExpectedHttpResponse(
            status_code=status.HTTP_200_OK,
            body=b'',
        ),
        mock__file_storage_api=mock__file_storage_api,
    )


@pytest.fixture(scope='session')
def test_case_failed_due_to_integrity_error() -> TestCaseFailedDueToIntegrityError:
    mock__fetch_catalog_item_price_and_picture_filename__return_value = CatalogItemPriceAndPictureFilenameResult(
        price=10,
        picture_filename='picture_filename',
    )

    catalog_item_request_data = CatalogItemRequestData(
        id=1,
        name='name',
        description='description',
        price=15,
        picture_filename='picture_filename',
        picture_url='picture_filename',
        catalog_type_id=1,
        catalog_brand_id=2,
        available_stock=10,
        restock_threshold=15,
        maxstock_threshold=20,
        on_reorder=False,
    )

    catalog_item_picture = fastapi.UploadFile(file=Mock(), filename='picture.jpeg')

    return TestCaseFailedDueToIntegrityError(
        catalog_item_request_data=catalog_item_request_data,
        catalog_item_picture=catalog_item_picture,
        mock__fetch_catalog_item_price_and_picture_filename__return_value=(
            mock__fetch_catalog_item_price_and_picture_filename__return_value
        ),
    )


@pytest.fixture(scope='session')
def test_case_failed_due_to_not_found_error() -> TestCaseFailedDueToIntegrityError:
    catalog_item_request_data = CatalogItemRequestData(
        id=1,
        name='name',
        description='description',
        price=15,
        picture_filename='picture_filename',
        picture_url='picture_filename',
        catalog_type_id=1,
        catalog_brand_id=2,
        available_stock=10,
        restock_threshold=15,
        maxstock_threshold=20,
        on_reorder=False,
    )

    catalog_item_picture = fastapi.UploadFile(file=Mock(), filename='picture.jpeg')

    return TestCaseFailedDueToNotFoundError(
        catalog_item_request_data=catalog_item_request_data,
        catalog_item_picture=catalog_item_picture,
    )


class TestUrlToView(TestClass[update_item]):
    def test(self):
        expected_url = '/catalog/items/'
        fact_url = CatalogAppConfig.get_api_router().url_path_for(update_item.__name__)
        assert fact_url == expected_url


class TestUpdateItemView(TestClass[update_item]):
    @patch.object(CatalogItemPriceChangedEvent, 'publish')
    @patch.object(view, '_update_catalog_item_in_db')
    @patch.object(view, '_fetch_catalog_item_price_and_picture_filename')
    def test_case_sucess_but_price_was_not_changed(
        self,
        mock__fetch_catalog_item_price_and_picture_filename: Mock,
        mock__update_catalog_item_in_db: Mock,
        mock__catalog_item_price_changed_event__publish: Mock,
        test_case_sucess_but_price_was_not_changed: TestCaseSuccessButPriceWasNotChanged,
    ):
        test_case = test_case_sucess_but_price_was_not_changed

        mock__fetch_catalog_item_price_and_picture_filename.return_value = (
            test_case.mock__fetch_catalog_item_price_and_picture_filename__return_value
        )

        mock__update_catalog_item_in_db.return_value = None

        mock__catalog_item_price_changed_event__publish.return_value = None

        with dependency_container.file_storage_api_factory.override(test_case.mock__file_storage_api):
            response = update_item(
                catalog_item_request_data=test_case.catalog_item_request_data,
                catalog_item_picture=test_case.catalog_item_picture,
            )

        assert response.status_code == test_case.expected_response.status_code
        assert response.body == test_case.expected_response.body

        mock__update_catalog_item_in_db.assert_called_once()

        mock__catalog_item_price_changed_event__publish.assert_not_called()

        cast(Mock, test_case.mock__file_storage_api.update).assert_called_once_with(
            old_file_filename=(
                test_case.mock__fetch_catalog_item_price_and_picture_filename__return_value.picture_filename
            ),
            upload_file=UploadFile(
                file=test_case.catalog_item_picture.file,
                filename=test_case.catalog_item_picture.filename,
            ),
            does_not_exist_ok=False,
        )

    @patch.object(CatalogItemPriceChangedEvent, 'publish', autospec=True)
    @patch.object(view, '_update_catalog_item_in_db')
    @patch.object(view, '_fetch_catalog_item_price_and_picture_filename')
    def test_case_success_but_price_has_been_changed(
        self,
        mock__fetch_catalog_item_price_and_picture_filename: Mock,
        mock__update_catalog_item_in_db: Mock,
        mock__catalog_item_price_changed_event__publish: Mock,
        test_case_success_but_price_has_been_changed: TestCaseSuccessButPriceHasBeenChanged,
    ):
        test_case = test_case_success_but_price_has_been_changed

        mock__fetch_catalog_item_price_and_picture_filename.return_value = (
            test_case.mock__fetch_catalog_item_price_and_picture_filename__return_value
        )

        mock__update_catalog_item_in_db.return_value = None

        mock__catalog_item_price_changed_event__publish.return_value = None

        with dependency_container.file_storage_api_factory.override(test_case.mock__file_storage_api):
            response = update_item(
                catalog_item_request_data=test_case.catalog_item_request_data,
                catalog_item_picture=test_case.catalog_item_picture,
            )

        assert response.status_code == test_case.expected_response.status_code
        assert response.body == test_case.expected_response.body

        mock__update_catalog_item_in_db.assert_called_once()

        fact_called_event: CatalogItemPriceChangedEvent = (
            mock__catalog_item_price_changed_event__publish.call_args[0][0]
        )
        assert fact_called_event == test_case.expected_published_event

        cast(Mock, test_case.mock__file_storage_api.update).assert_called_once_with(
            old_file_filename=(
                test_case.mock__fetch_catalog_item_price_and_picture_filename__return_value.picture_filename
            ),
            upload_file=UploadFile(
                file=test_case.catalog_item_picture.file,
                filename=test_case.catalog_item_picture.filename,
            ),
            does_not_exist_ok=False,
        )

    @patch.object(CatalogItemPriceChangedEvent, 'publish')
    @patch.object(view, '_update_catalog_item_in_db')
    @patch.object(view, '_fetch_catalog_item_price_and_picture_filename')
    def test_case_failed_due_to_integrity_error(
        self,
        mock__fetch_catalog_item_price_and_picture_filename: Mock,
        mock__update_catalog_item_in_db: Mock,
        mock__catalog_item_price_changed_event__publish: Mock,
        test_case_failed_due_to_integrity_error: TestCaseFailedDueToIntegrityError,
    ):
        test_case = test_case_failed_due_to_integrity_error

        mock__fetch_catalog_item_price_and_picture_filename.return_value = (
            test_case.mock__fetch_catalog_item_price_and_picture_filename__return_value
        )

        mock__update_catalog_item_in_db.side_effect = IntegrityError(orig=None, statement=None, params=None)

        mock__catalog_item_price_changed_event__publish.return_value = None

        mock__file_storage_api = Mock(spec=IFileStorageApi)

        with dependency_container.file_storage_api_factory.override(mock__file_storage_api):
            try:
                update_item(
                    catalog_item_request_data=test_case.catalog_item_request_data,
                    catalog_item_picture=test_case.catalog_item_picture,
                )
            except HTTPException as e:
                assert e.status_code == status.HTTP_400_BAD_REQUEST

        mock__update_catalog_item_in_db.assert_called_once()

        mock__catalog_item_price_changed_event__publish.assert_not_called()

        cast(Mock, mock__file_storage_api.update).assert_not_called()

    @patch.object(view, '_fetch_catalog_item_price_and_picture_filename')
    def test_case_failed_due_to_not_found_error(
        self,
        mock__fetch_catalog_item_price_and_picture_filename: Mock,
        test_case_failed_due_to_not_found_error: TestCaseFailedDueToNotFoundError,
    ):
        test_case = test_case_failed_due_to_not_found_error

        mock__fetch_catalog_item_price_and_picture_filename.side_effect = NotFoundError

        mock__file_storage_api = Mock(spec=IFileStorageApi)

        with dependency_container.file_storage_api_factory.override(mock__file_storage_api):
            try:
                update_item(
                    catalog_item_request_data=test_case.catalog_item_request_data,
                    catalog_item_picture=test_case.catalog_item_picture,
                )
            except HTTPException as e:
                assert e.status_code == status.HTTP_400_BAD_REQUEST

        cast(Mock, mock__file_storage_api.update).assert_not_called()
