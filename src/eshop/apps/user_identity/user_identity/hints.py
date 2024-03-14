from typing import NewType

UserId = NewType('UserId', int)
UserName = NewType('UserName', str)

# пароль в захешированном виде
HashedPassword = NewType('HashedPassword', str)
UserHashedPassword = NewType('UserHashedPassword', HashedPassword)

# пароль в явном виде
PlainPassword = NewType('PlainPassword', str)

JWTToken = NewType('JwtToken', str)
