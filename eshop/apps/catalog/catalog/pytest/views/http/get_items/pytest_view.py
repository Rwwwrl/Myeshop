from typing import List

from fastapi import HTTPException, status

from mock import Mock, patch

import pytest

from catalog.app_config import CatalogAppConfig
from catalog.domain.models import CatalogItem
from catalog.views.http.common.catalog_item_dto import CatalogItemDTO
from catalog.views.http.get_items import get_items, view

from framework.for_pytests.for_testing_http_views import ExpectedHttpResponseException
from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass


class TestInvalidRequestQueryParamsIds(TestCase['TestGetItemsView']):

    request_query_params__ids: str
    expected_http_response_exception: ExpectedHttpResponseException


class TestValidRequestQueryParamsIds(TestCase['TestGetItemsView']):

    request_query_params__ids: str
    expected_http_response: List[CatalogItemDTO]
    mock__fetch_catalog_items_from_db__return_value: List[CatalogItem]


class TestWithoutRequestQueryParamsIds(TestCase['TestGetItemsView']):

    expected_http_response: List[CatalogItemDTO]
    mock__fetch_catalog_items_from_db__return_value: List[CatalogItem]


@pytest.fixture(scope='session')
def test_invalid_request_query_params__ids() -> TestInvalidRequestQueryParamsIds:
    return TestInvalidRequestQueryParamsIds(
        request_query_params__ids='"not a list of int"',
        expected_http_response_exception=ExpectedHttpResponseException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='invalid query parameter "ids", must be a list of int',
        ),
    )


@pytest.fixture(scope='session')
def test_valid_request_query_params__ids() -> TestValidRequestQueryParamsIds:
    request_query_params__ids = '[1, 2, 3]'

    mock__fetch_catalog_items_from_db__return_value: List[CatalogItem] = [
        CatalogItem(
            id=1,
            name='name1',
            description='description1',
            price=10,
            picture_filename='picture_filename1',
            picture_url='picture_url1',
            available_stock=10,
            restock_threshold=20,
            maxstock_threshold=25,
            on_reorder=False,
            discount=0,
        ),
        CatalogItem(
            id=2,
            name='name2',
            description='description2',
            price=10,
            picture_filename='picture_filename2',
            picture_url='picture_url2',
            available_stock=10,
            restock_threshold=20,
            maxstock_threshold=25,
            on_reorder=False,
            discount=0,
        ),
    ]

    expected_http_response: List[CatalogItemDTO] = [
        CatalogItemDTO(
            id=1,
            name='name1',
            description='description1',
            price=10,
            picture_filename='picture_filename1',
            picture_url='picture_url1',
            available_stock=10,
            restock_threshold=20,
            maxstock_threshold=25,
            on_reorder=False,
            discount=0,
        ),
        CatalogItemDTO(
            id=2,
            name='name2',
            description='description2',
            price=10,
            picture_filename='picture_filename2',
            picture_url='picture_url2',
            available_stock=10,
            restock_threshold=20,
            maxstock_threshold=25,
            on_reorder=False,
            discount=0,
        ),
    ]

    return TestValidRequestQueryParamsIds(
        request_query_params__ids=request_query_params__ids,
        expected_http_response=expected_http_response,
        mock__fetch_catalog_items_from_db__return_value=mock__fetch_catalog_items_from_db__return_value,
    )


@pytest.fixture(scope='session')
def test_without_request_query_params__ids() -> TestWithoutRequestQueryParamsIds:
    mock__fetch_catalog_items_from_db__return_value: List[CatalogItem] = [
        CatalogItem(
            id=1,
            name='name1',
            description='description1',
            price=10,
            picture_filename='picture_filename1',
            picture_url='picture_url1',
            available_stock=10,
            restock_threshold=20,
            maxstock_threshold=25,
            on_reorder=False,
            discount=0,
        ),
        CatalogItem(
            id=2,
            name='name2',
            description='description2',
            price=10,
            picture_filename='picture_filename2',
            picture_url='picture_url2',
            available_stock=10,
            restock_threshold=20,
            maxstock_threshold=25,
            on_reorder=False,
            discount=0,
        ),
    ]

    expected_http_response: List[CatalogItemDTO] = [
        CatalogItemDTO(
            id=1,
            name='name1',
            description='description1',
            price=10,
            picture_filename='picture_filename1',
            picture_url='picture_url1',
            available_stock=10,
            restock_threshold=20,
            maxstock_threshold=25,
            on_reorder=False,
            discount=0,
        ),
        CatalogItemDTO(
            id=2,
            name='name2',
            description='description2',
            price=10,
            picture_filename='picture_filename2',
            picture_url='picture_url2',
            available_stock=10,
            restock_threshold=20,
            maxstock_threshold=25,
            on_reorder=False,
            discount=0,
        ),
    ]

    return TestWithoutRequestQueryParamsIds(
        expected_http_response=expected_http_response,
        mock__fetch_catalog_items_from_db__return_value=mock__fetch_catalog_items_from_db__return_value,
    )


class TestUrlToView(TestClass[get_items]):
    def test(self):
        expected_url = '/catalog/items/'
        fact_url = CatalogAppConfig.get_api_router().url_path_for(get_items.__name__)
        assert fact_url == expected_url


class TestGetItemsView(TestClass[get_items]):
    def test_invalid_request_query_params__ids(
        self,
        test_invalid_request_query_params__ids: TestInvalidRequestQueryParamsIds,
    ):
        test_case = test_invalid_request_query_params__ids

        try:
            get_items(ids=test_case.request_query_params__ids)
        except HTTPException as e:
            assert e.status_code == test_case.expected_http_response_exception.status_code
            assert e.detail == test_case.expected_http_response_exception.detail

    @patch.object(view, view._fetch_catalog_items_from_db.__name__)
    def test_valid_request_query_params__ids(
        self,
        mock__fetch_catalog_items_from_db: Mock,
        test_valid_request_query_params__ids: TestValidRequestQueryParamsIds,
    ):
        test_case = test_valid_request_query_params__ids

        mock__fetch_catalog_items_from_db.return_value = test_case.mock__fetch_catalog_items_from_db__return_value

        response = get_items(ids=test_case.request_query_params__ids)
        assert response == test_case.expected_http_response

        mock__fetch_catalog_items_from_db.assert_called_once_with(ids=[1, 2, 3])

    @patch.object(view, view._fetch_catalog_items_from_db.__name__)
    def test_without_request_query_params__ids(
        self,
        mock__fetch_catalog_items_from_db: Mock,
        test_without_request_query_params__ids: TestWithoutRequestQueryParamsIds,
    ):
        test_case = test_without_request_query_params__ids

        mock__fetch_catalog_items_from_db.return_value = test_case.mock__fetch_catalog_items_from_db__return_value

        response = get_items()
        assert response == test_case.expected_http_response

        mock__fetch_catalog_items_from_db.assert_called_once_with(ids=None)
