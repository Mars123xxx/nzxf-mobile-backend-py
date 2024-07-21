from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import SessionLocal
from schema.base import ErrorResponse
from schema.user import LoginResponse, LoginRequest
from service.user import get_user_service

api_user = APIRouter(tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@api_user.post('/login', response_model=LoginResponse | ErrorResponse)
async def login(r: LoginRequest,db: Session = Depends(get_db)):
    srv = get_user_service()
    return srv.login(r,db)
