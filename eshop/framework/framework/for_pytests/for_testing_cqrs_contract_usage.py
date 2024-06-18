import abc
from typing import TypeVar

from framework.for_pytests.test_class import TestClass

QueryClsTypeVar = TypeVar('QueryClsTypeVar')


class ITestQueryContract(abc.ABC, TestClass[QueryClsTypeVar]):
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
