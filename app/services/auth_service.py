from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token

def register_user(db: Session, name: str, phone: str, password: str, role: str, email: str | None = None):
    # Check if phone exists
    if db.query(User).filter(User.phone == phone).first():
        return None, "Phone already registered"

    hashed = hash_password(password)
    new_user = User(
        name=name,
        phone=phone,
        email=email,
        password_hash=hashed,
        role=UserRole.RESIDENT if role.lower() == "resident" else UserRole.SECURITY
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Include role in JWT payload
    token = create_access_token({
        "sub": str(new_user.id),
        "role": new_user.role.value  # This is the key change
    })
    return new_user, token


def authenticate_user(db: Session, phone: str, password: str):
    user = db.query(User).filter(User.phone == phone).first()
    if not user or not verify_password(password, user.password_hash):
        return None

    # Include role in JWT payload
    token = create_access_token({
        "sub": str(user.id),
        "role": user.role.value
    })
    return user, token
