import abc
from typing import Any, Type, TypeVar, Union

import attrs

from pydantic import BaseModel

from pytest_check import check

from framework.for_pytests.test_class import TestClass

QueryClsTypeVar = TypeVar('QueryClsTypeVar')
CommandClsTypeVar = TypeVar('CommandClsTypeVar')


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


class ITestCommandContract(abc.ABC, TestClass[CommandClsTypeVar]):
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


class AttributeValidator:
    @staticmethod
    def _is_pydantic_cls(validating_cls: Type) -> bool:
        return issubclass(validating_cls, BaseModel)

    @staticmethod
    def _is_attrs_cls(validating_cls: Type) -> bool:
        return attrs.has(validating_cls)

    @staticmethod
    def _assert_attribute__attrs(
        validating_cls: Type[attrs.AttrsInstance],
        attribute_name: str,
        expected_type: Any,
    ) -> None:
        with check:
            assert hasattr(attrs.fields(validating_cls), attribute_name)
            assert getattr(attrs.fields(validating_cls), attribute_name).type == expected_type

    @staticmethod
    def _assert_attribute__pydantic(
        validating_cls: Type[BaseModel],
        attribute_name: str,
        expected_type: Any,
    ) -> None:
        with check:
            assert validating_cls.model_fields.get(attribute_name, None) is not None
            assert validating_cls.model_fields[attribute_name].annotation == expected_type

    def __call__(
        self,
        validating_cls: Union[Type[attrs.AttrsInstance], Type[BaseModel]],
        attribute_name: str,
        expected_type: Any,
    ) -> None:
        """
        Проверяем, что у `validating_cls` есть атрибут с именем `attribute_name` и его тип равен `expected_type`
        """
        if self._is_pydantic_cls(validating_cls):
            self._assert_attribute__pydantic(
                validating_cls=validating_cls,
                attribute_name=attribute_name,
                expected_type=expected_type,
            )
            return

        if self._is_attrs_cls(validating_cls):
            self._assert_attribute__attrs(
                validating_cls=validating_cls,
                attribute_name=attribute_name,
                expected_type=expected_type,
            )
            return

        raise ValueError('validation_cls must be either Type[pydantic.BaseModel] or Type[attrs.AttrsInstance]')


assert_attribute = AttributeValidator()
