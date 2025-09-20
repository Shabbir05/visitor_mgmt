from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserOut
from app.models.user import User
from app.utils.dependencies import get_current_user

from fastapi import APIRouter, Depends
from app.utils.dependencies import get_current_user

router = APIRouter()

@router.get("/debug/me")
def debug_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "role": current_user.role
    }

# Get current user
@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# List all residents (example)
@router.get("/residents", response_model=list[UserOut])
def list_residents(db: Session = Depends(get_db)):
    return db.query(User).filter(User.role == "resident").all()
