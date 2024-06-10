from framework.common.dto import DTO

from user_identity_cqrs_contract.hints import UserId


class UserDTO(DTO):

    id: UserId
