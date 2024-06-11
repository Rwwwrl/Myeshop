from typing import NewType

# TODO в задаче ESHOP-48 это заменится на pydantic.FieldTypes

CustomerId = NewType('CustomerId', int)

BasketItemId = NewType('BasketItemId', int)
ProductId = NewType('ProductId', int)

ProductName = NewType('ProductName', str)
Price = NewType('Price', float)
Quantity = NewType('Quantity', int)
PictureUrl = NewType('PictureUrl', str)
