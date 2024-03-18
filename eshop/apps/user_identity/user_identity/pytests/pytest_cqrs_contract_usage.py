import pytest

from pytest_check import check

from user_identity_cqrs_contract.hints import JWTToken
from user_identity_cqrs_contract.query.query import UserIdFromJWTTokenQuery
from user_identity_cqrs_contract.query.query_response import (
    UserDTO,
    UserId,
)


@pytest.mark.cqrs_contract_usage
class TestUserIdFromJWTTokenQuery:
    def test_query(self):
        with check:
            assert UserIdFromJWTTokenQuery.model_fields.get('jwt_token', None)
            assert UserIdFromJWTTokenQuery.model_fields['jwt_token'].annotation == JWTToken

    def test_response(self):
        response_type = UserIdFromJWTTokenQuery.get_response_type()

        with check:
            assert response_type == UserDTO
            assert UserDTO.model_fields.get('id', None)
            assert UserDTO.model_fields['id'].annotation == UserId
