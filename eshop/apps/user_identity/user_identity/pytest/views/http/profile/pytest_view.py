from mock import Mock, patch

import pytest

from framework.for_pytests.test_case import TestCase as _TestCase
from framework.for_pytests.test_class import TestClass

from user_identity import hints
from user_identity.api_router import api_router
from user_identity.infrastructure.peristance.user import UserORM, UserRepository
from user_identity.views.http.profile import profile
from user_identity.views.http.profile.view import ProfileDTO


class TestCase(_TestCase['TestCaseProfileView']):

    user_id: hints.UserId
    mock__user_repository__get_by_id__return_value: UserORM
    expected_response: ProfileDTO


@pytest.fixture(scope='session')
def test_case() -> TestCase:
    user_id = 1

    mock__user_repository__get_by_id__return_value = UserORM(
        id=1,
        name='name',
        hashed_password='hashed_password',
    )

    expected_response = ProfileDTO(
        id=1,
        name='name',
    )

    return TestCase(
        user_id=user_id,
        mock__user_repository__get_by_id__return_value=mock__user_repository__get_by_id__return_value,
        expected_response=expected_response,
    )


class TestUrlToView(TestClass[profile]):
    def test(self):
        expected_url = '/user_identity/profile/'
        fact_url = api_router.url_path_for(profile.__name__)
        assert fact_url == expected_url


class TestCaseProfileView(TestClass[profile]):
    @patch.object(UserRepository, 'get_by_id')
    def test_case_user_exist(
        self,
        mock__user_repository__get_by_id: Mock,
        test_case: TestCase,
    ):
        mock__user_repository__get_by_id.return_value = test_case.mock__user_repository__get_by_id__return_value

        response = profile(user_id=test_case.user_id)
        assert response == test_case.expected_response

        mock__user_repository__get_by_id.assert_called_once_with(id=test_case.user_id)
