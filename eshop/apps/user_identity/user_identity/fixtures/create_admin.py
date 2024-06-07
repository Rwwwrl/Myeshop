from framework.sqlalchemy.session_factory import session_factory

from user_identity.dependency_container import dependency_container
from user_identity.domain.models.user import User


def create_admin():
    with session_factory() as session:
        hashed_password = dependency_container.password_hasher_factory().hash(plain_password='1234')

        user = User(name='admin', hashed_password=hashed_password)
        session.add(user)

        session.commit()


if __name__ == '__main__':
    create_admin()
