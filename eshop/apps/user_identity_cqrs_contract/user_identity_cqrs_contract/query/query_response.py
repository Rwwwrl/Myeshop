from framework.common.dto import DTO

from user_identity_cqrs_contract import hints


class UserDTO(DTO):

    id: hints.UserId
    name: hints.UserName
