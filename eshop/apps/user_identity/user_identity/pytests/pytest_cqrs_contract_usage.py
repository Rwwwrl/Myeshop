import attrs

import pytest

from pytest_check import check

from framework.for_pytests.for_testing_cqrs_contract_usage import ITestQueryContract

from user_identity_cqrs_contract.hints import JWTToken
from user_identity_cqrs_contract.query.query import UserIdFromJWTTokenQuery
from user_identity_cqrs_contract.query.query_response import (
    UserDTO,
    UserId,
)


@pytest.mark.cqrs_contract_usage
class TestUserIdFromJWTTokenQuery(ITestQueryContract[UserIdFromJWTTokenQuery]):
    def test_query_contract(self):
        with check:
            assert hasattr(attrs.fields(UserIdFromJWTTokenQuery), 'jwt_token')
            assert attrs.fields(UserIdFromJWTTokenQuery).jwt_token.type == JWTToken

    def test_query_response_contract(self):
        response_type = UserIdFromJWTTokenQuery.__response_type__()

        with check:
            assert response_type == UserDTO
            assert UserDTO.model_fields.get('id', None) is not None
            assert UserDTO.model_fields['id'].annotation == UserId
