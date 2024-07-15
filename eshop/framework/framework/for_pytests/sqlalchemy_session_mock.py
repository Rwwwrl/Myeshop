from mock import Mock


class SqlalchemySessionMock(Mock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commit = Mock()
        self.expunge = Mock()

    def __enter__(self, *args, **kwargs) -> 'SqlalchemySessionMock':
        return self

    def __exit__(self, *args, **kwargs) -> None:
        pass
