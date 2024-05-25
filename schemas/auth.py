import typing
from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class Payload(BaseModel):
    sub: str
    role: str
    iat: int


class CustomResponse(BaseModel):
    success: bool
    code: int
    message: str
    data: typing.Union[typing.Dict[str, typing.Any], typing.List[typing.Any], None]


class RegisterForm(BaseModel):
    username: str
    email: str
    password: str


class LoginForm(BaseModel):
    identifier: str
    password: str

