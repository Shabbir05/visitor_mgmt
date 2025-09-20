from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

# User roles
class UserRole(str, enum.Enum):
    RESIDENT = "resident"
    SECURITY = "security"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), unique=True, nullable=False)   # mandatory
    email = Column(String(100), unique=True, nullable=True)   # optional for security
    password_hash = Column(String(255), nullable=False)       # store hashed password
    role = Column(Enum(UserRole), nullable=False)
