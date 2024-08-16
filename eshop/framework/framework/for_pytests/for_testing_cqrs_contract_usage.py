import abc
import types
import typing as t
from datetime import datetime, timedelta
from typing import Any, Type, TypeVar, Union

import attrs

from pydantic import BaseModel

import pytest

from pytest_check import check

from framework.common.dto import DTO
from framework.cqrs.command import ISyncCommand
from framework.cqrs.context import IContext
from framework.cqrs.event import IEvent
from framework.cqrs.query import IQuery
from framework.for_pytests.test_class import TestClass

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


class ITestEventContract(abc.ABC, TestClass[EventTypeVar], metaclass=TestConctractMetaUnionWithABCMeta):
    """
    Базовый класс для тестирования контракта команды
    """
    @abc.abstractmethod
    def test_event_contract(self) -> None:
        """
        тестируем контракт самой квери
        """
        raise NotImplementedError


class ThisComplexTypeIsNotYetSupported:
    pass


def _get_fact_type_from_complex_type(complex_type: Any) -> Any:
    """
    функция получения 'fact_type' из 'complex_type'

    посмотреть примеры можно в
        framework.pytests.for_pytests.pytest_for_testing_cqrs_contract_usage.TestGetFactTypeFromComplexType
    """

    fact_types = set([int, float, str, set, list, dict, tuple, datetime, timedelta])
    if complex_type in fact_types:
        return complex_type

    if isinstance(complex_type, t._AnnotatedAlias):
        # к этому относится Annotated
        return _get_fact_type_from_complex_type(complex_type.__origin__)

    if isinstance(complex_type, t._UnionGenericAlias):
        if complex_type._name == 'Union':
            return t.Union[*[_get_fact_type_from_complex_type(arg) for arg in complex_type.__args__]]    # type: ignore

        if complex_type._name == 'Optional':
            return t.Optional[_get_fact_type_from_complex_type(complex_type.__args__[0])]

        # set | int является инстансом types.UnionType, но
        # t.NewType('name', str) | t.NewType('name', int) ялвяется инстансом typing.Union
        # при этом _name = None, но _origin указывает на typing.Union
        if complex_type.__origin__ is t.Union:
            # TODO: пока что не придумал как возвращать в таком же ввиде через "|",
            # пока что возвращаю через typing.Union
            return t.Union[*[_get_fact_type_from_complex_type(arg) for arg in complex_type.__args__]]    # type: ignore

    if isinstance(complex_type, t.NewType):
        return _get_fact_type_from_complex_type(complex_type.__supertype__)

    if isinstance(complex_type, types.UnionType):
        # относится к такой записи "int | str"

        # TODO: пока что не придумал как возвращать в таком же ввиде через "|",
        # пока что возвращаю через typing.Union
        return t.Union[*[_get_fact_type_from_complex_type(arg) for arg in complex_type.__args__]]    # type: ignore

    if isinstance(complex_type, types.GenericAlias):
        if complex_type.__origin__ is list:
            return list[_get_fact_type_from_complex_type(complex_type.__args__[0])]

        if complex_type.__origin__ is dict:
            return dict[
                _get_fact_type_from_complex_type(complex_type.__args__[0]),
                _get_fact_type_from_complex_type(complex_type.__args__[1]),
            ]

        if complex_type.__origin__ is set:
            return set[_get_fact_type_from_complex_type(complex_type.__args__[0])]

        if complex_type.__origin__ is tuple:
            return tuple[_get_fact_type_from_complex_type(complex_type.__args__[0])]

    if isinstance(complex_type, t._GenericAlias):
        # к t._GenericAlias относятся все typing.List, typing.Dict, typing.Set
        if complex_type.__origin__ is list:
            return t.List[_get_fact_type_from_complex_type(complex_type.__args__[0])]

        if complex_type.__origin__ is dict:
            return t.Dict[
                _get_fact_type_from_complex_type(complex_type.__args__[0]),
                _get_fact_type_from_complex_type(complex_type.__args__[1]),
            ]

        if complex_type.__origin__ is set:
            return t.Set[_get_fact_type_from_complex_type(complex_type.__args__[0])]

        if complex_type.__origin__ is tuple:
            return t.Tuple[_get_fact_type_from_complex_type(complex_type.__args__[0])]

    if issubclass(complex_type, IContext):
        return complex_type

    if issubclass(complex_type, DTO):
        return complex_type

    raise ThisComplexTypeIsNotYetSupported(f'complex_type = {complex_type}')


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
        expected_fact_type: Any,
    ) -> None:
        with check:
            assert hasattr(attrs.fields(validating_cls), attribute_name)

            fact_type = _get_fact_type_from_complex_type(getattr(attrs.fields(validating_cls), attribute_name).type)
            assert fact_type == expected_fact_type

    @staticmethod
    def _assert_attribute__pydantic(
        validating_cls: Type[BaseModel],
        attribute_name: str,
        expected_fact_type: Any,
    ) -> None:
        with check:
            assert validating_cls.model_fields.get(attribute_name, None) is not None

            fact_type = _get_fact_type_from_complex_type(validating_cls.model_fields[attribute_name].annotation)
            assert fact_type == expected_fact_type

    def __call__(
        self,
        validating_cls: Union[Type[attrs.AttrsInstance], Type[BaseModel]],
        attribute_name: str,
        expected_fact_type: Any,
    ) -> None:
        """
        Проверяем, что у `validating_cls` есть атрибут с именем `attribute_name`
        и его 'фактический тип'* равен `expected_type`

        что значит "фактический тип" смотреть тут
        https://www.notion.so/rwwwrl/cqrs-6d2febc0faa541a6906ba22e6ef2f2e0?pvs=4

        """
        if self._is_pydantic_cls(validating_cls):
            self._assert_attribute__pydantic(
                validating_cls=validating_cls,
                attribute_name=attribute_name,
                expected_fact_type=expected_fact_type,
            )
            return

        if self._is_attrs_cls(validating_cls):
            self._assert_attribute__attrs(
                validating_cls=validating_cls,
                attribute_name=attribute_name,
                expected_fact_type=expected_fact_type,
            )
            return

        raise ValueError('validation_cls must be either Type[pydantic.BaseModel] or Type[attrs.AttrsInstance]')


assert_attribute = AttributeValidator()
