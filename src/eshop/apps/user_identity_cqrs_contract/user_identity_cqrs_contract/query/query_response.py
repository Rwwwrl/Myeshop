from eshop.framework.ddd.dto import DTO

from user_identity_cqrs_contract.types import UserId


class UserDTO(DTO):

    id: UserId
