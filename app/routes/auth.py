from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterUser, LoginUser, Token
from app.models.user import User, UserRole
from app.database import get_db
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token

router = APIRouter()

# Register
@router.post("/register", response_model=Token)
def register(user: RegisterUser, db: Session = Depends(get_db)):
    # Check if phone/email already exists
    if db.query(User).filter(User.phone == user.phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered")

    hashed = hash_password(user.password)
    new_user = User(
        name=user.name,
        phone=user.phone,
        email=user.email,
        password_hash=hashed,
        role=UserRole.RESIDENT if user.role.lower() == "resident" else UserRole.SECURITY
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Include role in JWT
    access_token = create_access_token({
        "sub": str(new_user.id),
        "role": new_user.role.value  # use .value since role is an Enum
    })
    return {"access_token": access_token, "token_type": "bearer"}

# Login
@router.post("/login", response_model=Token)
def login(credentials: LoginUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == credentials.phone).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Include role in JWT
    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role.value
    })
    return {"access_token": access_token, "token_type": "bearer"}
