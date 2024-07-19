from typing import List

from mock import Mock, patch

import pytest

from catalog.infrastructure.persistance.postgres.models import CatalogBrandORM, CatalogItemORM, CatalogTypeORM
from catalog.views.cqrs.query_handlers import CatalogItemByIdQueryHandler

from catalog_cqrs_contract.query import CatalogItemsByIdsQuery
from catalog_cqrs_contract.query.query_response import (
    CatalogBrandDTO,
    CatalogItemDTO,
    CatalogTypeDTO,
)

from framework.for_pytests.test_case import TestCase as _TestCase
from framework.for_pytests.test_class import TestClass


class TestCase(_TestCase['TestCatalogItemByIdQueryHandler__handle']):

    query: CatalogItemsByIdsQuery
    mock__fetch_from_db__return_value: List[CatalogItemORM]
    expected_result: List[CatalogItemDTO]


@pytest.fixture(scope='session')
def test_case() -> TestClass:
    query = CatalogItemsByIdsQuery(ids=[1, 2, 3])

    catalog_brand = CatalogBrandORM(id=1, brand='brand')
    catalog_type = CatalogTypeORM(id=1, type='type')
    mock__fetch_from_db__return_value: List[CatalogItemORM] = [
        CatalogItemORM(
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
            catalog_type=catalog_type,
            catalog_brand=catalog_brand,
        ),
        CatalogItemORM(
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
            catalog_type=catalog_type,
            catalog_brand=catalog_brand,
        ),
    ]

    catalog_brand_dto = CatalogBrandDTO(
        id=1,
        brand='brand',
    )
    catalog_type_dto = CatalogTypeDTO(
        id=1,
        type='type',
    )
    expected_result: List[CatalogItemDTO] = [
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
            catalog_type=catalog_type_dto,
            catalog_brand=catalog_brand_dto,
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
            catalog_type=catalog_type_dto,
            catalog_brand=catalog_brand_dto,
        ),
    ]

    return TestCase(
        query=query,
        mock__fetch_from_db__return_value=mock__fetch_from_db__return_value,
        expected_result=expected_result,
    )


class TestCatalogItemByIdQueryHandler__handle(TestClass[CatalogItemByIdQueryHandler.handle]):
    @patch.object(CatalogItemByIdQueryHandler, '_fetch_from_db')
    def test(self, mock__fetch_from_db: Mock, test_case: TestCase):

        mock__fetch_from_db.return_value = test_case.mock__fetch_from_db__return_value

        result = CatalogItemByIdQueryHandler().handle(query=test_case.query)
        assert result == test_case.expected_result

        mock__fetch_from_db.assert_called_once_with(ids=test_case.query.ids)
