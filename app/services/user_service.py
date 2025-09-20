from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def list_residents(db: Session):
    return db.query(User).filter(User.role == "resident").all()
