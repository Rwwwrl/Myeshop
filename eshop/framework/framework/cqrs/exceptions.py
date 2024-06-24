from typing import final


class CQRSException(Exception):
    pass


class PossibleExpectedError(CQRSException):
    pass


@final
class UnexpectedError(CQRSException):
    def __init__(self, *args, original_exception: Exception, **kwargs):
        self._original_exception_cls_name = original_exception.__class__.__name__
        self._original_exception_message = str(original_exception)
