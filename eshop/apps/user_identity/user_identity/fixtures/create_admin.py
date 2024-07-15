from framework.sqlalchemy.session import Session

from user_identity.dependency_container import dependency_container
from user_identity.infrastructure.peristance.user import UserORM


def create_admin():
    with Session() as session:
        hashed_password = dependency_container.password_hasher_factory().hash(plain_password='1234')

        user = UserORM(id=1, name='admin', hashed_password=hashed_password)
        session.add(user)

        session.commit()


if __name__ == '__main__':
    create_admin()
