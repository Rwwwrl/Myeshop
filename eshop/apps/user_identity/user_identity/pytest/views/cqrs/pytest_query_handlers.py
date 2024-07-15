from mock import Mock, patch

import pytest

from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass

from user_identity.infrastructure.peristance.user import UserORM, UserRepository, user_repository
from user_identity.views.cqrs.query_handlers import UserQueryHandler

from user_identity_cqrs_contract.query import (
    UserQuery,
    query as query_module,
)
from user_identity_cqrs_contract.query.query_response import UserDTO


class TestCaseUserExist(TestCase['TestUserQueryHandler__handle']):

    query: UserQuery
    mock__user_repository__get_by_id__return_value: UserORM
    expected_response: UserDTO


class TestCaseUserDoesNotExist(TestCase['TestUserQueryHandler__handle']):

    query: UserQuery


@pytest.fixture(scope='session')
def test_case_user_exist() -> TestCaseUserExist:
    query = UserQuery(user_id=1)

    mock__user_repository__get_by_id__return_value = UserORM(id=1, name='name', hashed_password='hashed_password')

    expected_response = UserDTO(id=1, name='name')

    return TestCaseUserExist(
        query=query,
        mock__user_repository__get_by_id__return_value=mock__user_repository__get_by_id__return_value,
        expected_response=expected_response,
    )


@pytest.fixture(scope='session')
def test_case_user_does_not_exist() -> TestCaseUserDoesNotExist:
    query = UserQuery(user_id=1)

    return TestCaseUserDoesNotExist(query=query)


class TestUserQueryHandler__handle(TestClass[UserQueryHandler.handle]):
    @patch.object(UserRepository, 'get_by_id')
    def test_case_user_exist(
        self,
        mock__user_repository__get_by_id: Mock,
        test_case_user_exist: TestCaseUserExist,
    ):
        test_case = test_case_user_exist

        mock__user_repository__get_by_id.return_value = test_case.mock__user_repository__get_by_id__return_value

        response = UserQueryHandler().handle(query=test_case.query)
        assert response == test_case.expected_response

        mock__user_repository__get_by_id.assert_called_once_with(id=test_case.query.user_id)

    @patch.object(UserRepository, 'get_by_id')
    def test_case_user_does_not_exist(
        self,
        mock__user_repository__get_by_id: Mock,
        test_case_user_does_not_exist: TestCaseUserDoesNotExist,
    ):
        test_case = test_case_user_does_not_exist

        mock__user_repository__get_by_id.side_effect = user_repository.NotFoundError

        try:
            UserQueryHandler().handle(query=test_case.query)
        except Exception as e:
            assert isinstance(e, query_module.UserNotFoundError)

        mock__user_repository__get_by_id.assert_called_once_with(id=test_case.query.user_id)
