import re

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from datetime import timedelta, datetime
from jose import jwt
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.types import ASGIApp

from const import code
from const.msg import get_msg
from schema.base import ErrorResponse
from schema.user import UserBase

SECRET_KEY = "R3F5G8H9J1K2^!M6N8O7P1@$%2R3S4T5U6V9W8X0Y1Z"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10  # 十分钟
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7天
ISSUER = "nzxf"


def create_token(user: UserBase) -> (str, str):
    access_token_exp = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_exp = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    claims = {
        'id': user.id,
        'username': user.username,
        'issuer': ISSUER,
        'exp': access_token_exp
    }

    access_token = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode({
        'issuer': ISSUER,
        'exp': refresh_token_exp
    }, SECRET_KEY, algorithm=ALGORITHM)

    return access_token, refresh_token


def get_token(request: Request) -> (str, str):
    headers = dict(request.scope['headers'])
    return headers.get('x-token', ''), headers.get('x-refresh-token', '')


def parse_token(token: str) -> dict:
    claims = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return claims


def check_token(access_token: str, refresh_token: str) -> (str, str):
    # 检查完会返回两个新的access_token,refresh_token
    claims_access = parse_token(access_token)
    claims_refresh = parse_token(refresh_token)

    if claims_access['exp'] > datetime.now():
        # 如果access没有过期
        return create_token(UserBase(id=claims_access['id'], username=claims_access['username']))
    # access过期了,但是refresh没有过期
    if claims_refresh['exp'] > datetime.now():
        return create_token(UserBase(id=claims_access['id'], username=claims_access['username']))
    # 两者都过期了,重新登录
    return "", ""


def set_token(response:Response,new_access_token: str, new_refresh_token: str):
    response.headers['x-token'] = new_access_token
    response.headers['x-refresh-token'] = new_refresh_token


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response | JSONResponse:
        # 接收来自客户端的Request请求
        path = request.scope['path']
        obj = re.compile(r'^/api/user/(login|register)')
        if obj.match(path) and not re.match(r'^/(api/)?$', path):
            response = await call_next(request)
            return response
        access_token, refresh_token = get_token(request)
        if access_token == "":
            return JSONResponse(content=
                                ErrorResponse(
                                    code=code.NOT_ACCESS_TOKEN_ERROR,
                                    detail=get_msg(code.NOT_ACCESS_TOKEN_ERROR)).dict())
        new_access_token, new_refresh_token = check_token(access_token, refresh_token)
        if new_access_token == "" and new_refresh_token == "":
            return JSONResponse(content=
                                ErrorResponse(
                                    code=code.ALL_TOKEN_EXPIRED,
                                    detail=get_msg(code.ALL_TOKEN_EXPIRED)).dict())
        response = await call_next(request)
        set_token(response, new_access_token, new_refresh_token)
        return response
