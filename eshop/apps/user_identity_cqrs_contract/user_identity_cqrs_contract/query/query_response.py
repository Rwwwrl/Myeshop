from enum import Enum

from framework.common.dto import DTO

from user_identity_cqrs_contract import hints


class UserRoleEnum(Enum):
    ADMIN = 'ADMIN'
    CUSTOMER = 'CUSTOMER'


class UserIdWithRoleDTO(DTO):
    id: hints.UserId
    role: UserRoleEnum


class UserDTO(DTO):

    id: hints.UserId
    name: hints.UserName
