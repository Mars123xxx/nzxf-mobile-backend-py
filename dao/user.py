from sqlalchemy.orm import Session

from db import models


def get_user_by_phone(db: Session, phone: int):
    return db.query(models.User).filter_by(phone=phone).first()
