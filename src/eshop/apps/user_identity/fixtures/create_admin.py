from sqlalchemy.orm import Session

from eshop import settings
from eshop.apps.user_identity.dependency_container import dependency_container
from eshop.apps.user_identity.domain.models.user import User


def create_admin():
    with Session(settings.SQLALCHEMY_ENGINE) as session:
        hashed_password = dependency_container.password_hasher_factory().hash(plain_password='1234')

        user = User(name='admin', hashed_password=hashed_password)
        session.add(user)

        session.commit()


if __name__ == '__main__':
    create_admin()
