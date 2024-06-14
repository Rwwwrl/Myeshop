from typing import Any

from attrs import define

import mock

import pytest

from framework.common.dto import DTO
from framework.cqrs import registry
from framework.cqrs.cqrs_bus import CQRSBus
from framework.cqrs.query import IQuery, IQueryHandler, Query
from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass


class MockQueryResponse(DTO):
    value: int


@define
class MockQuery(Query[MockQueryResponse]):
    arg: int


class MockQueryHandler(IQueryHandler):
    def handle(self, query: MockQuery) -> MockQueryResponse:
        return MockQueryResponse(value=query.arg)


@pytest.fixture(scope='session')
def patch_registry():
    patched_registry = registry.Registry()
    patched_registry.register(MockQuery, MockQueryHandler)

    patch = mock.patch.object(registry, 'get_registry')
    mock_get_registry = patch.start()
    mock_get_registry.return_value = patched_registry
    yield
    patch.stop()


class FetchTestCase(TestCase['TestCQRSBus__fetch']):

    query: IQuery
    query_result: Any


@pytest.fixture(scope='session')
def fetch_use_case() -> FetchTestCase:
    return FetchTestCase(
        query=MockQuery(arg=10),
        query_result=MockQueryResponse(value=10),
    )


class TestCQRSBus__fetch(TestClass[CQRSBus.fetch]):
    def test(
        self,
        fetch_use_case: FetchTestCase,
        patch_registry: None,
    ):
        cqrs_bus = CQRSBus()
        query_result = cqrs_bus.fetch(query=fetch_use_case.query)
        assert query_result == fetch_use_case.query_result
