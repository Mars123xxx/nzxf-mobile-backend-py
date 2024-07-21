from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    username: str


class UserInfo(UserBase):
    nickname: str
    phone: int
    sex: bool
    avatar: str


class AuthToken(BaseModel):
    access_token: str
    refresh_token: str


class LoginRequest(BaseModel):
    phone: int
    password: str
    # captcha: str 验证码


class LoginResponse(UserInfo, AuthToken):
    ...
