import typing as t
from datetime import datetime, timedelta
from enum import Enum

import pytest

import pytest_lazyfixture

from framework.common.dto import DTO
from framework.cqrs.context import IContext
from framework.for_pytests.for_testing_cqrs_contract_usage import _get_fact_type_from_complex_type
from framework.for_pytests.test_case import TestCase as _TestCase
from framework.for_pytests.test_class import TestClass


class TestCase(_TestCase['TestGetFactTypeFromComplexType']):
    complex_type: t.Any
    expected_fact_type: t.Any


@pytest.fixture(scope='session', params=[int, float, str, set, list, dict, tuple, datetime, timedelta])
def test_case_fact_types(request) -> TestCase:
    return TestCase(complex_type=request.param, expected_fact_type=request.param)


@pytest.fixture(scope='session')
def test_case_float() -> TestCase:
    return TestCase(complex_type=float, expected_fact_type=float)


@pytest.fixture(scope='session')
def test_case_NewType() -> TestCase:
    return TestCase(complex_type=t.NewType('name', int), expected_fact_type=int)


@pytest.fixture(scope='session')
def test_case_Annotated() -> TestCase:
    return TestCase(complex_type=t.Annotated[int, 'description'], expected_fact_type=int)


@pytest.fixture(scope='session')
def test_case_typing_List() -> TestCase:
    return TestCase(complex_type=t.List[t.NewType('name', int)], expected_fact_type=t.List[int])    # noqa


@pytest.fixture(scope='session')
def test_case_list() -> TestCase:
    return TestCase(complex_type=list[t.NewType('name', int)], expected_fact_type=list[int])    # noqa


@pytest.fixture(scope='session')
def test_case_typing_Dict() -> TestCase:
    return TestCase(
        complex_type=t.Dict[t.NewType('name', str), t.NewType('name', int)],    # noqa
        expected_fact_type=t.Dict[str, int],
    )


@pytest.fixture(scope='session')
def test_case_dict() -> TestCase:
    return TestCase(
        complex_type=dict[t.NewType('name', str), t.NewType('name', int)],    # noqa
        expected_fact_type=dict[str, int],
    )


@pytest.fixture(scope='session')
def test_case_typing_Set() -> TestCase:
    return TestCase(
        complex_type=t.Set[t.NewType('name', str)],    # noqa
        expected_fact_type=t.Set[str],
    )


@pytest.fixture(scope='session')
def test_case_set() -> TestCase:
    return TestCase(
        complex_type=set[t.NewType('name', str)],    # noqa
        expected_fact_type=set[str],
    )


@pytest.fixture(scope='session')
def test_case_typing_Tuple() -> TestCase:
    return TestCase(
        complex_type=t.Tuple[t.NewType('name', str)],    # noqa
        expected_fact_type=t.Tuple[str],
    )


@pytest.fixture(scope='session')
def test_case_tuple() -> TestCase:
    return TestCase(
        complex_type=tuple[t.NewType('name', str)],    # noqa
        expected_fact_type=tuple[str],
    )


@pytest.fixture(scope='session')
def test_case_typing_Union() -> TestCase:
    return TestCase(
        complex_type=t.Union[
            t.NewType('name', str),    # noqa
            t.NewType('name', int),    # noqa
            t.NewType('name', set),    # noqa
        ],
        expected_fact_type=t.Union[str, int, set],
    )


@pytest.fixture(scope='session')
def test_case_union1() -> TestCase:
    return TestCase(
        complex_type=str | int | set,
        expected_fact_type=t.Union[str, int, set],
    )


@pytest.fixture(scope='session')
def test_case_union2() -> TestCase:
    complex_type = t.NewType('name', str) | t.NewType('name', int) | t.NewType('name', set)
    expected_fact_type = t.Union[str, int, set]
    return TestCase(complex_type=complex_type, expected_fact_type=expected_fact_type)


@pytest.fixture(scope='session')
def test_case_typing_Optional() -> TestCase:
    return TestCase(
        complex_type=t.Optional[t.NewType('name', str)],    # noqa
        expected_fact_type=t.Optional[str],
    )


@pytest.fixture(scope='session')
def test_case_typing_Enum() -> TestCase:
    class MyEnum(Enum):
        pass

    return TestCase(
        complex_type=MyEnum,
        expected_fact_type=MyEnum,
    )


@pytest.fixture(scope='session')
def test_case_pydantic_BaseModel() -> TestCase:
    class MyDTO(DTO):
        field1: str

    return TestCase(complex_type=MyDTO, expected_fact_type=MyDTO)


@pytest.fixture(scope='session')
def test_case_context() -> TestCase:
    class MyContext(IContext):
        field1: str

    return TestCase(complex_type=MyContext, expected_fact_type=MyContext)


@pytest.fixture(scope='session')
def test_case_super_complex_type() -> TestCase:
    class MyDTO(DTO):
        field1: str

    # yapf: disable
    complex_type = t.Dict[
        t.NewType('name', str), # noqa
        list[
            t.Dict[
                int,
                t.Tuple[
                    t.Dict[
                        t.Set[
                            t.Dict[
                                t.NewType(
                                    'name',  # noqa
                                    set[t.Annotated[t.NewType('name', str), 'description']], # noqa
                                ),
                                float,
                                ],
                            ],
                        set[MyDTO],
                        ],
                    ],
                ],
            ],
        ]
    # yapf: enable

    # yapf: disable
    expected_fact_type = t.Dict[
        str,
        list[
            t.Dict[
                int,
                t.Tuple[
                    t.Dict[
                        t.Set[
                            t.Dict[
                                set[str],
                                float,
                            ],
                        ],
                        set[MyDTO],
                    ],
                ],
            ],
        ],
    ]
    # yapf: enable

    return TestCase(complex_type=complex_type, expected_fact_type=expected_fact_type)


@pytest.fixture(
    scope='session',
    params=[
        pytest_lazyfixture.lazy_fixture(test_case_fact_types.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_NewType.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_Annotated.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_typing_List.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_list.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_typing_Dict.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_dict.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_typing_Set.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_set.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_typing_Tuple.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_tuple.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_typing_Union.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_union1.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_union2.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_typing_Optional.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_typing_Enum.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_super_complex_type.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_pydantic_BaseModel.__name__),
        pytest_lazyfixture.lazy_fixture(test_case_context.__name__),
    ],
)
def test_case(request) -> TestCase:
    return request.param


class TestGetFactTypeFromComplexType(TestClass[_get_fact_type_from_complex_type]):
    def test(self, test_case: TestCase):
        fact_type = _get_fact_type_from_complex_type(complex_type=test_case.complex_type)
        assert fact_type == test_case.expected_fact_type
