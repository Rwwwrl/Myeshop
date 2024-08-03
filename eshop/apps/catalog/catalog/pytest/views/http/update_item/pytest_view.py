from fastapi import HTTPException, status

from mock import Mock, patch

from pydantic.types import PositiveFloat

import pytest

from sqlalchemy.exc import IntegrityError

from catalog.app_config import CatalogAppConfig
from catalog.views.http.update_item import update_item, view
from catalog.views.http.update_item.view import CatalogItemRequestData, NotFoundError

from catalog_cqrs_contract.event import CatalogItemPriceChangedEvent

from framework.cqrs.context import InsideSqlachemySessionContext
from framework.for_pytests.for_testing_http_views import ExpectedHttpResponse
from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass
from framework.sqlalchemy.session import Session


class TestCaseSuccessButPriceWasNotChanged(TestCase['TestUpdateItemView']):
    mock__fetch_current_catalog_item_price__return_value: PositiveFloat
    catalog_item_request_data: CatalogItemRequestData
    expected_response: ExpectedHttpResponse


class TestCaseSuccessButPriceHasBeenChanged(TestCase['TestUpdateItemView']):
    mock__fetch_current_catalog_item_price__return_value: PositiveFloat
    catalog_item_request_data: CatalogItemRequestData
    expected_published_event: CatalogItemPriceChangedEvent
    expected_response: ExpectedHttpResponse


class TestCaseFailedDueToIntegrityError(TestCase['TestUpdateItemView']):
    mock__fetch_current_catalog_item_price__return_value: PositiveFloat
    catalog_item_request_data: CatalogItemRequestData


class TestCaseFailedDueToNotFoundError(TestCase['TestUpdateItemView']):
    catalog_item_request_data: CatalogItemRequestData


@pytest.fixture(scope='session')
def test_case_sucess_but_price_was_not_changed() -> TestCaseSuccessButPriceWasNotChanged:
    mock__fetch_current_catalog_item_price__return_value = 10

    catalog_item_request_data = CatalogItemRequestData(
        id=1,
        name='name',
        description='description',
        price=mock__fetch_current_catalog_item_price__return_value,
        picture_filename='picture_filename',
        picture_url='picture_filename',
        catalog_type_id=1,
        catalog_brand_id=2,
        available_stock=10,
        restock_threshold=15,
        maxstock_threshold=20,
        on_reorder=False,
    )

    return TestCaseSuccessButPriceWasNotChanged(
        catalog_item_request_data=catalog_item_request_data,
        mock__fetch_current_catalog_item_price__return_value=mock__fetch_current_catalog_item_price__return_value,
        expected_response=ExpectedHttpResponse(
            status_code=status.HTTP_200_OK,
            body=b'',
        ),
    )


@pytest.fixture(scope='session')
def test_case_success_but_price_has_been_changed() -> TestCaseSuccessButPriceHasBeenChanged:
    mock__fetch_current_catalog_item_price__return_value = 10

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

    expected_published_event = CatalogItemPriceChangedEvent(
        catalog_item_id=1,
        old_price=10,
        new_price=15,
        context=InsideSqlachemySessionContext(session=Session()),
    )

    return TestCaseSuccessButPriceHasBeenChanged(
        catalog_item_request_data=catalog_item_request_data,
        mock__fetch_current_catalog_item_price__return_value=mock__fetch_current_catalog_item_price__return_value,
        expected_published_event=expected_published_event,
        expected_response=ExpectedHttpResponse(
            status_code=status.HTTP_200_OK,
            body=b'',
        ),
    )


@pytest.fixture(scope='session')
def test_case_failed_due_to_integrity_error() -> TestCaseFailedDueToIntegrityError:
    mock__fetch_current_catalog_item_price__return_value = 10

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

    return TestCaseFailedDueToIntegrityError(
        catalog_item_request_data=catalog_item_request_data,
        mock__fetch_current_catalog_item_price__return_value=mock__fetch_current_catalog_item_price__return_value,
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

    return TestCaseFailedDueToNotFoundError(catalog_item_request_data=catalog_item_request_data)


class TestUrlToView(TestClass[update_item]):
    def test(self):
        expected_url = '/catalog/items/'
        fact_url = CatalogAppConfig.get_api_router().url_path_for(update_item.__name__)
        assert fact_url == expected_url


class TestUpdateItemView(TestClass[update_item]):
    @patch.object(CatalogItemPriceChangedEvent, 'publish')
    @patch.object(view, '_update_catalog_item_in_db')
    @patch.object(view, '_fetch_current_catalog_item_price')
    def test_case_sucess_but_price_was_not_changed(
        self,
        mock__fetch_current_catalog_item_price: Mock,
        mock__update_catalog_item_in_db: Mock,
        mock__catalog_item_price_changed_event__publish: Mock,
        test_case_sucess_but_price_was_not_changed: TestCaseSuccessButPriceWasNotChanged,
    ):
        test_case = test_case_sucess_but_price_was_not_changed

        mock__fetch_current_catalog_item_price.return_value = (
            test_case.mock__fetch_current_catalog_item_price__return_value
        )

        mock__update_catalog_item_in_db.return_value = None

        mock__catalog_item_price_changed_event__publish.return_value = None

        response = update_item(catalog_item_request_data=test_case.catalog_item_request_data)
        assert response.status_code == test_case.expected_response.status_code
        assert response.body == test_case.expected_response.body

        mock__update_catalog_item_in_db.assert_called_once()

        mock__catalog_item_price_changed_event__publish.assert_not_called()

    @patch.object(CatalogItemPriceChangedEvent, 'publish', autospec=True)
    @patch.object(view, '_update_catalog_item_in_db')
    @patch.object(view, '_fetch_current_catalog_item_price')
    def test_case_success_but_price_has_been_changed(
        self,
        mock__fetch_current_catalog_item_price: Mock,
        mock__update_catalog_item_in_db: Mock,
        mock__catalog_item_price_changed_event__publish: Mock,
        test_case_success_but_price_has_been_changed: TestCaseSuccessButPriceHasBeenChanged,
    ):
        test_case = test_case_success_but_price_has_been_changed

        mock__fetch_current_catalog_item_price.return_value = (
            test_case.mock__fetch_current_catalog_item_price__return_value
        )

        mock__update_catalog_item_in_db.return_value = None

        mock__catalog_item_price_changed_event__publish.return_value = None

        response = update_item(catalog_item_request_data=test_case.catalog_item_request_data)
        assert response.status_code == test_case.expected_response.status_code
        assert response.body == test_case.expected_response.body

        mock__update_catalog_item_in_db.assert_called_once()

        fact_called_event: CatalogItemPriceChangedEvent = (
            mock__catalog_item_price_changed_event__publish.call_args[0][0]
        )
        assert fact_called_event == test_case.expected_published_event

    @patch.object(CatalogItemPriceChangedEvent, 'publish')
    @patch.object(view, '_update_catalog_item_in_db')
    @patch.object(view, '_fetch_current_catalog_item_price')
    def test_case_failed_due_to_integrity_error(
        self,
        mock__fetch_current_catalog_item_price: Mock,
        mock__update_catalog_item_in_db: Mock,
        mock__catalog_item_price_changed_event__publish: Mock,
        test_case_failed_due_to_integrity_error: TestCaseFailedDueToIntegrityError,
    ):
        test_case = test_case_failed_due_to_integrity_error

        mock__fetch_current_catalog_item_price.return_value = (
            test_case.mock__fetch_current_catalog_item_price__return_value
        )

        mock__update_catalog_item_in_db.side_effect = IntegrityError(orig=None, statement=None, params=None)

        mock__catalog_item_price_changed_event__publish.return_value = None

        try:
            update_item(catalog_item_request_data=test_case.catalog_item_request_data)
        except HTTPException as e:
            assert e.status_code == status.HTTP_400_BAD_REQUEST

        mock__update_catalog_item_in_db.assert_called_once()
        mock__catalog_item_price_changed_event__publish.assert_not_called()

    @patch.object(view, '_fetch_current_catalog_item_price')
    def test_case_failed_due_to_not_found_error(
        self,
        mock__fetch_current_catalog_item_price: Mock,
        test_case_failed_due_to_not_found_error: TestCaseFailedDueToNotFoundError,
    ):
        test_case = test_case_failed_due_to_not_found_error

        mock__fetch_current_catalog_item_price.side_effect = NotFoundError

        try:
            update_item(catalog_item_request_data=test_case.catalog_item_request_data)
        except HTTPException as e:
            assert e.status_code == status.HTTP_400_BAD_REQUEST
