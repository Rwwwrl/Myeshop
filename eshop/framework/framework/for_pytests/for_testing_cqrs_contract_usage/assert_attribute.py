import contextlib
import types
import typing as t
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Type, Union

import attrs

from pydantic import BaseModel

from pytest_check import check

from framework.common.dto import DTO
from framework.cqrs.context import IContext


class ThisComplexTypeIsNotYetSupported:
    pass


class FactTypeFromComplexTypeGetter:
    @classmethod
    def _get_from_typing_module(cls, complex_type: Any) -> Any:
        if isinstance(complex_type, t._AnnotatedAlias):
            # к этому относится Annotated
            return cls.get(complex_type.__origin__)

        if isinstance(complex_type, t._UnionGenericAlias):
            if complex_type._name == 'Union':
                args = [cls.get(arg) for arg in complex_type.__args__]
                return t.Union[*args]    # type: ignore

            if complex_type._name == 'Optional':
                return t.Optional[cls.get(complex_type.__args__[0])]

            # set | int является инстансом types.UnionType, но
            # t.NewType('name', str) | t.NewType('name', int) ялвяется инстансом typing.Union
            # при этом _name = None, но _origin указывает на typing.Union
            if complex_type.__origin__ is t.Union:
                # TODO: пока что не придумал как возвращать в таком же ввиде через "|",
                # пока что возвращаю через typing.Union
                args = [cls.get(arg) for arg in complex_type.__args__]
                return t.Union[*args]    # type: ignore # noqa

        if isinstance(complex_type, t.NewType):
            return cls.get(complex_type.__supertype__)

        if isinstance(complex_type, t._GenericAlias):
            # к t._GenericAlias относятся все typing.List, typing.Dict, typing.Set
            if complex_type.__origin__ is list:
                return t.List[cls.get(complex_type.__args__[0])]

            if complex_type.__origin__ is dict:
                return t.Dict[
                    cls.get(complex_type.__args__[0]),
                    cls.get(complex_type.__args__[1]),
                ]

            if complex_type.__origin__ is set:
                return t.Set[cls.get(complex_type.__args__[0])]

            if complex_type.__origin__ is tuple:
                return t.Tuple[cls.get(complex_type.__args__[0])]

    @classmethod
    def _get_from_stdlib(cls, complex_type: Any) -> Any:
        if isinstance(complex_type, types.UnionType):
            # относится к такой записи "int | str"

            # TODO: пока что не придумал как возвращать в таком же ввиде через "|",
            # пока что возвращаю через typing.Union
            return t.Union[*[cls.get(arg) for arg in complex_type.__args__]]    # type: ignore

        if isinstance(complex_type, types.GenericAlias):
            if complex_type.__origin__ is list:
                return list[cls.get(complex_type.__args__[0])]

            if complex_type.__origin__ is dict:
                return dict[cls.get(complex_type.__args__[0]), cls.get(complex_type.__args__[1])]

            if complex_type.__origin__ is set:
                return set[cls.get(complex_type.__args__[0])]

            if complex_type.__origin__ is tuple:
                return tuple[cls.get(complex_type.__args__[0])]

        if issubclass(complex_type, Enum):
            return complex_type

    @classmethod
    def _get_from_custom_types(cls, complex_type: Any) -> Any:
        with contextlib.suppress(TypeError):
            if issubclass(complex_type, IContext):
                return complex_type

        with contextlib.suppress(TypeError):
            if issubclass(complex_type, DTO):
                return complex_type

    @classmethod
    def get(cls, complex_type: Any) -> Any:
        """
        функция получения 'fact_type' из 'complex_type'

        посмотреть примеры можно в
            framework.pytests.for_pytests.pytest_for_testing_cqrs_contract_usage.TestGetFactTypeFromComplexType
        """
        fact_types = set([int, float, str, set, list, dict, tuple, datetime, timedelta])
        if complex_type in fact_types:
            return complex_type

        result = cls._get_from_custom_types(complex_type)
        if result is not None:
            return result

        result = cls._get_from_typing_module(complex_type)
        if result is not None:
            return result

        result = cls._get_from_stdlib(complex_type)
        if result is not None:
            return result

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

            fact_type = FactTypeFromComplexTypeGetter.get(getattr(attrs.fields(validating_cls), attribute_name).type)
            assert fact_type == expected_fact_type

    @staticmethod
    def _assert_attribute__pydantic(
        validating_cls: Type[BaseModel],
        attribute_name: str,
        expected_fact_type: Any,
    ) -> None:
        with check:
            assert validating_cls.model_fields.get(attribute_name, None) is not None

            fact_type = FactTypeFromComplexTypeGetter.get(validating_cls.model_fields[attribute_name].annotation)
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
