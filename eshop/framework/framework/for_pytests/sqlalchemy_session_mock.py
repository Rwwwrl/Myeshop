from mock import Mock


class SqlalchemySessionMock(Mock):
    def __enter__(self, *args, **kwargs) -> 'SqlalchemySessionMock':
        return self

    def __exit__(self, *args, **kwargs) -> None:
        pass
