from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from mock import Mock, patch

import pytest

from framework.for_pytests.for_testing_http_views import ExpectedHttpResponseException
from framework.for_pytests.test_case import TestCase
from framework.for_pytests.test_class import TestClass

from user_identity import hints
from user_identity.api_router import api_router
from user_identity.views.http.token import token, view
from user_identity.views.http.token.view import AccessTokenDTO, AuthenticateException, TokenType


class TestCaseLoginSucess(TestCase['TestTokenView']):

    mock__login__return_value: hints.JWTToken
    expected_response: AccessTokenDTO
    form_data: OAuth2PasswordRequestForm


class TestCaseLoginFailed(TestCase['TestTokenView']):

    form_data: OAuth2PasswordRequestForm
    expected_response_exception: ExpectedHttpResponseException


@pytest.fixture(scope='session')
def test_case_login_success() -> TestCaseLoginSucess:
    mock__login__return_value = hints.JWTToken('1111')

    expected_response = AccessTokenDTO(
        access_token=hints.JWTToken('1111'),
        token_type=TokenType.bearer,
    )

    form_data = OAuth2PasswordRequestForm(username='username', password='password')

    return TestCaseLoginSucess(
        mock__login__return_value=mock__login__return_value,
        expected_response=expected_response,
        form_data=form_data,
    )


@pytest.fixture(scope='session')
def test_case_login_failed() -> TestCaseLoginFailed:
    form_data = OAuth2PasswordRequestForm(username='username', password='password')

    return TestCaseLoginFailed(
        form_data=form_data,
        expected_response_exception=ExpectedHttpResponseException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ),
    )


class TestUrlToView(TestClass[token]):
    def test(self):
        expected_url = '/user_identity/token/'
        fact_url = api_router.url_path_for(token.__name__)
        assert fact_url == expected_url


class TestTokenView(TestClass[token]):
    @patch.object(view, 'login')
    def test_case_login_success(
        self,
        mock__login: Mock,
        test_case_login_success: TestCaseLoginSucess,
    ):
        test_case = test_case_login_success

        mock__login.return_value = test_case.mock__login__return_value

        response = token(form_data=test_case.form_data)
        assert response == test_case.expected_response

    @patch.object(view, 'login')
    def test_case_login_failed(
        self,
        mock__login: Mock,
        test_case_login_failed: TestCaseLoginFailed,
    ):
        test_case = test_case_login_failed

        mock__login.side_effect = AuthenticateException

        try:
            token(form_data=test_case.form_data)
        except HTTPException as e:
            assert e.status_code == test_case.expected_response_exception.status_code
            assert e.detail == test_case.expected_response_exception.detail
            assert e.headers == test_case.expected_response_exception.headers
