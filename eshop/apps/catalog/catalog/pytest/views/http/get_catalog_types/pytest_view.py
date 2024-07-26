from typing import List

from mock import Mock, patch

import pytest

from catalog.app_config import CatalogAppConfig
from catalog.infrastructure.persistance.postgres.models import CatalogTypeORM
from catalog.views.http.get_catalog_types import get_catalog_types, view
from catalog.views.http.get_catalog_types.dto import CatalogTypeDTO

from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass


class TestCase(TestCase['TestGetCatalogTypesView']):
    mock__fetch_all_catalog_types_from_db__return_value: List[CatalogTypeORM]
    expected_response: List[CatalogTypeDTO]


@pytest.fixture(scope='session')
def test_case() -> TestCase:

    mock__fetch_all_catalog_types_from_db__return_value: List[CatalogTypeORM] = [
        CatalogTypeORM(
            id=1,
            type='type1',
        ),
        CatalogTypeORM(
            id=2,
            type='type2',
        ),
    ]

    expected_response: List[CatalogTypeDTO] = [
        CatalogTypeDTO(id=1, type='type1'),
        CatalogTypeDTO(id=2, type='type2'),
    ]

    return TestCase(
        mock__fetch_all_catalog_types_from_db__return_value=mock__fetch_all_catalog_types_from_db__return_value,
        expected_response=expected_response,
    )


class TestUrlToView(TestClass[get_catalog_types]):
    def test(self):
        expected_url = '/catalog/catalog_types/'
        fact_url = CatalogAppConfig.get_api_router().url_path_for(get_catalog_types.__name__)
        assert fact_url == expected_url


class TestGetCatalogTypesView(TestClass[get_catalog_types]):
    @patch.object(view, '_fetch_all_catalog_types_from_db')
    def test(
        self,
        mock__fetch_all_catalog_types_from_db: Mock,
        test_case: TestCase,
    ):
        mock__fetch_all_catalog_types_from_db.return_value = (
            test_case.mock__fetch_all_catalog_types_from_db__return_value
        )

        response = get_catalog_types()
        assert response == test_case.expected_response

        mock__fetch_all_catalog_types_from_db.assert_called_once_with()
