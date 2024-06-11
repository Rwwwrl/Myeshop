from typing import Generic, TypeVar

TestObjectTypeVar = TypeVar('TestObjectTypeVar')


class TestClass(Generic[TestObjectTypeVar]):
    """
    нужен только для аннотации и подсказки другим разработчикам:
    через TestTypeObjectVar мы указываем что именно тестирует класс.

    пример 1:
    class TestMyQueryHandler(TestClass[MyQueryHandler]) - тут мы говорим, что объектом тестирования является класс
    `MyQueryHandler`

    пример 2:
    class TestMyQueryHandler__handler(TestClass[MyQueryHandler.handle]) - тут мы говорим, что объектом тестирования
    является метод `handle` класса `MyQueryHandler`
    """
