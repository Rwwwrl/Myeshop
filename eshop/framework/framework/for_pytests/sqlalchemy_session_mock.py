from mock import Mock


class SqlalchemySessionMock(Mock):
    commit = Mock()
    expunge = Mock()

    def __enter__(self, *args, **kwargs) -> 'SqlalchemySessionMock':
        return self

    def __exit__(self, *args, **kwargs) -> None:
        pass
