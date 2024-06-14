from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

TestCaseClsTypeVar = TypeVar('TestCaseClsTypeVar')


class TestCase(BaseModel, Generic[TestCaseClsTypeVar], frozen=True):
    """
    юз кейс для теста `TestCaseClsTypeVar`
    """

    __test__ = False

    model_config = ConfigDict(arbitrary_types_allowed=True)
