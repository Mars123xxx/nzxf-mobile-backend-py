from sqlalchemy.orm import Session

from const import code
from const.msg import get_msg
from dao.user import get_user_by_phone
from db.database import SessionLocal
from middleware.auth import create_token
from schema.base import ErrorResponse
from schema.user import LoginRequest, LoginResponse, UserBase


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def login(r: LoginRequest, db: Session) -> LoginResponse | ErrorResponse:
        user = get_user_by_phone(db, r.phone)
        if user is None:
            return ErrorResponse(code=code.USER_EXISTS_ERROR, detail=get_msg(code.USER_EXISTS_ERROR))
        if not user.check_password(r.password):
            return ErrorResponse(code=code.LOGIN_PASSWORD_ERROR, detail=get_msg(code.LOGIN_PASSWORD_ERROR))
        access_token, refresh_token = create_token(UserBase(id=user.id, username=user.username))
        return LoginResponse(access_token=access_token,
                             refresh_token=refresh_token,
                             id=user.id,
                             sex=user.sex,
                             username=user.username,
                             nickname=user.nickname,
                             avatar=user.avatar,
                             phone=user.phone)


def get_user_service() -> UserService:
    return UserService()
