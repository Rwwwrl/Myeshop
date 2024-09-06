from typing import List

from mock import Mock, patch

import pytest

from catalog import hints
from catalog.app_config import CatalogAppConfig
from catalog.domain.models import CatalogItem
from catalog.views.http.common.catalog_item_dto import CatalogItemDTO
from catalog.views.http.get_items_by_type_id_and_brand_id import get_items_by_type_id_and_brand_id, view

from framework.common.dto import DTO
from framework.for_pytests.test_case import TestCase as _TestCase
from framework.for_pytests.test_class import TestClass


class RequestQueryParams(DTO):
    brand_id: hints.CatalogBrandId
    type_id: hints.CatalogTypeId


class TestCase(_TestCase['TestGetItemsByTypeIdAndBrandIdView']):

    request_query_params: RequestQueryParams
    expected_http_response: List[CatalogItemDTO]
    mock__fetch_catalog_items_from_db__return_value: List[CatalogItem]


@pytest.fixture(scope='session')
def test_case() -> TestCase:
    request_query_params = RequestQueryParams(brand_id=1, type_id=2)

    mock__fetch_catalog_items_from_db__return_value: List[CatalogItem] = [
        CatalogItem(
            id=1,
            name='name1',
            description='description1',
            price=10,
            picture_filename='picture_filename1',
            picture_url='picture_url1',
            catalog_type_id=1,
            catalog_brand_id=2,
            available_stock=10,
            restock_threshold=20,
            maxstock_threshold=25,
            on_reorder=False,
            discount=10,
        ),
        CatalogItem(
            id=2,
            name='name2',
            description='description2',
            price=10,
            picture_filename='picture_filename2',
            picture_url='picture_url2',
            catalog_type_id=3,
            catalog_brand_id=4,
            available_stock=10,
            restock_threshold=20,
            maxstock_threshold=25,
            on_reorder=False,
            discount=20,
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
            catalog_type_id=1,
            catalog_brand_id=2,
            available_stock=10,
            restock_threshold=20,
            maxstock_threshold=25,
            on_reorder=False,
            discount=10,
        ),
        CatalogItemDTO(
            id=2,
            name='name2',
            description='description2',
            price=10,
            picture_filename='picture_filename2',
            picture_url='picture_url2',
            catalog_type_id=3,
            catalog_brand_id=4,
            available_stock=10,
            restock_threshold=20,
            maxstock_threshold=25,
            on_reorder=False,
            discount=20,
        ),
    ]

    return TestCase(
        request_query_params=request_query_params,
        expected_http_response=expected_http_response,
        mock__fetch_catalog_items_from_db__return_value=mock__fetch_catalog_items_from_db__return_value,
    )


class TestUrlToView(TestClass[get_items_by_type_id_and_brand_id]):
    def test(self):
        brand_id = 1
        type_id = 2

        expected_url = f'/catalog/items/type/{type_id}/brand/{brand_id}/'
        fact_url = CatalogAppConfig.get_api_router().url_path_for(
            get_items_by_type_id_and_brand_id.__name__,
            brand_id=brand_id,
            type_id=type_id,
        )
        assert fact_url == expected_url


class TestGetItemsByTypeIdAndBrandIdView(TestClass[get_items_by_type_id_and_brand_id]):
    @patch.object(view, '_fetch_catalog_items_from_db')
    def test_case(
        self,
        mock__fetch_catalog_items_from_db: Mock,
        test_case: TestCase,
    ):
        mock__fetch_catalog_items_from_db.return_value = test_case.mock__fetch_catalog_items_from_db__return_value

        response = get_items_by_type_id_and_brand_id(
            brand_id=test_case.request_query_params.brand_id,
            type_id=test_case.request_query_params.type_id,
        )
        assert response == test_case.expected_http_response

        mock__fetch_catalog_items_from_db.assert_called_once_with(
            type_id=test_case.request_query_params.type_id,
            brand_id=test_case.request_query_params.brand_id,
        )
