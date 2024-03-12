from typing import NewType

UserId = NewType('UserId', int)
UserName = NewType('UserName', str)
# пароль пользователя в захешированном виде
UserHashedPassword = NewType('UserHashedPassword', str)

# пароль в явном виде
PlainPassword = NewType('PlainPassword', str)

JWTToken = NewType('JwtToken', str)
