import abc
from typing import TypeVar

import pytest

from framework.cqrs.command import ISyncCommand
from framework.cqrs.event import IEvent
from framework.cqrs.query import IQuery
from framework.for_pytests.test_class import TestClass

__all__ = (
    'ITestQueryContract',
    'ITestSyncCommandContract',
    'ITestEventContractPublisher',
    'ITestEventContractConsumer',
)

QueryTypeVar = TypeVar('QueryTypeVar', bound=IQuery)
SyncCommandTypeVar = TypeVar('SyncCommandTypeVar', bound=ISyncCommand)
EventTypeVar = TypeVar('EventTypeVar', bound=IEvent)


class TestContractMeta(type):
    """
    класс нужен только для того чтобы автоматически навешивать pytest.mark.cqrs_contract_usag
    на каждый класс теста контракта.
    """
    def __new__(cls, *args, **kwargs):
        return pytest.mark.cqrs_contract_usage(super().__new__(cls, *args, **kwargs))


class TestConctractMetaUnionWithABCMeta(TestContractMeta, abc.ABCMeta):
    """нужно для решения проблемы 'metaclass conflict'"""


class ITestQueryContract(abc.ABC, TestClass[QueryTypeVar], metaclass=TestConctractMetaUnionWithABCMeta):
    """
    Базовый класс для тестирования контракта квери
    """
    @abc.abstractmethod
    def test_query_contract(self) -> None:
        """
        тестируем контракт самой квери
        """
        raise NotImplementedError

    @abc.abstractmethod
    def test_query_response_contract(self) -> None:
        """
        тестируем контракт ответа
        """
        raise NotImplementedError


class ITestSyncCommandContract(abc.ABC, TestClass[SyncCommandTypeVar], metaclass=TestConctractMetaUnionWithABCMeta):
    """
    Базовый класс для тестирования контракта команды
    """
    @abc.abstractmethod
    def test_command_contract(self) -> None:
        """
        тестируем контракт самой квери
        """
        raise NotImplementedError

    @abc.abstractmethod
    def test_command_response_contract(self) -> None:
        """
        тестируем контракт ответа
        """
        raise NotImplementedError


class ITestEventContractPublisher(abc.ABC, TestClass[EventTypeVar], metaclass=TestConctractMetaUnionWithABCMeta):
    """
    Базовый класс для тестирования контракта эвента со стороны publisher`a
    """
    @abc.abstractmethod
    def test_event_contract(self) -> None:
        """
        тестируем контракт самой квери
        """
        raise NotImplementedError


class ITestEventContractConsumer(abc.ABC, TestClass[EventTypeVar], metaclass=TestConctractMetaUnionWithABCMeta):
    """
    Базовый класс для тестирования контракта эвента со стороны consumer`а
    """
    @abc.abstractmethod
    def test_event_contract(self) -> None:
        """
        тестируем контракт самой квери
        """
        raise NotImplementedError
