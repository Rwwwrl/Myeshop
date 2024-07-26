from eshop.settings import SETTINGS

from framework.sqlalchemy.session import Session

from user_identity.dependency_container import dependency_container
from user_identity.infrastructure.peristance.user import UserORM


def create_admin():
    hashed_password = dependency_container.password_hasher_factory().hash(
        plain_password=SETTINGS.user_identity_service.initial_admin_user_credentials.password,
    )
    user = UserORM(
        name=SETTINGS.user_identity_service.initial_admin_user_credentials.name,
        hashed_password=hashed_password,
    )

    with Session() as session:
        with session.begin():
            session.add(user)


if __name__ == '__main__':
    create_admin()
