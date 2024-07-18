from sqlalchemy.orm import sessionmaker

from eshop.settings import SQLALCHEMY_ENGINE

Session = sessionmaker(SQLALCHEMY_ENGINE, autobegin=False)
