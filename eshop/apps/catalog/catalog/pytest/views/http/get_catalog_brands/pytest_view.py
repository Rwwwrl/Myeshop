from typing import List

from mock import Mock, patch

import pytest

from catalog.app_config import CatalogAppConfig
from catalog.infrastructure.persistance.postgres.models import CatalogBrandORM
from catalog.views.http.get_catalog_brands import get_catalog_brands, view
from catalog.views.http.get_catalog_brands.dto import CatalogBrandDTO

from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass


class TestCase(TestCase['TestGetCatalogTypesView']):
    mock__fetch_all_catalog_brands_from_db__return_value: List[CatalogBrandORM]
    expected_response: List[CatalogBrandDTO]


@pytest.fixture(scope='session')
def test_case() -> TestCase:

    mock__fetch_all_catalog_types_from_db__return_value: List[CatalogBrandDTO] = [
        CatalogBrandORM(
            id=1,
            brand='brand1',
        ),
        CatalogBrandORM(
            id=2,
            brand='brand2',
        ),
    ]

    expected_response: List[CatalogBrandDTO] = [
        CatalogBrandDTO(id=1, brand='brand1'),
        CatalogBrandDTO(id=2, brand='brand2'),
    ]

    return TestCase(
        mock__fetch_all_catalog_brands_from_db__return_value=mock__fetch_all_catalog_types_from_db__return_value,
        expected_response=expected_response,
    )


class TestUrlToView(TestClass[get_catalog_brands]):
    def test(self):
        expected_url = '/catalog/catalog_brands/'
        fact_url = CatalogAppConfig.get_api_router().url_path_for(get_catalog_brands.__name__)
        assert fact_url == expected_url


class TestGetCatalogTypesView(TestClass[get_catalog_brands]):
    @patch.object(view, '_fetch_all_catalog_brands_from_db')
    def test(
        self,
        mock__fetch_all_catalog_brands_from_db: Mock,
        test_case: TestCase,
    ):
        mock__fetch_all_catalog_brands_from_db.return_value = (
            test_case.mock__fetch_all_catalog_brands_from_db__return_value
        )

        response = get_catalog_brands()
        assert response == test_case.expected_response

        mock__fetch_all_catalog_brands_from_db.assert_called_once_with()
