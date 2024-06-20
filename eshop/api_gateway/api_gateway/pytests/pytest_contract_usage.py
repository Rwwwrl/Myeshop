from typing import List

import attrs

import pytest

from pytest_check import check

import catalog_cqrs_contract.hints
from catalog_cqrs_contract.query import CatalogItemsByIdsQuery
from catalog_cqrs_contract.query.query_response import CatalogItemDTO

from framework.for_pytests.for_testing_cqrs_contract_usage import ITestQueryContract


@pytest.mark.cqrs_contract_usage
class TestCatalogItemByIdsQuery(ITestQueryContract[CatalogItemsByIdsQuery]):
    def test_query_contract(self):
        with check:
            assert hasattr(attrs.fields(CatalogItemsByIdsQuery), 'ids')
            assert attrs.fields(CatalogItemsByIdsQuery).ids.type == List[catalog_cqrs_contract.hints.CatalogItemId]

    def test_query_response_contract(self):
        response_type = CatalogItemsByIdsQuery.__response_type__()

        with check:
            assert response_type == List[CatalogItemDTO]

            assert CatalogItemDTO.model_fields.get('id', None) is not None
            assert CatalogItemDTO.model_fields['id'].annotation == catalog_cqrs_contract.hints.CatalogItemId

            assert CatalogItemDTO.model_fields.get('name', None) is not None
            assert CatalogItemDTO.model_fields['name'].annotation == str

            assert CatalogItemDTO.model_fields.get('price', None) is not None
            assert CatalogItemDTO.model_fields['price'].annotation == float

            assert CatalogItemDTO.model_fields.get('picture_url', None) is not None
            assert CatalogItemDTO.model_fields['picture_url'].annotation == str
