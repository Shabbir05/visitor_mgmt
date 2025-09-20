from pydantic import BaseModel, EmailStr, constr

# Register user
class RegisterUser(BaseModel):
    name: str
    phone: constr(min_length=10, max_length=15)
    email: EmailStr | None = None
    password: str
    role: str  # 'resident' or 'security'

# Login user
class LoginUser(BaseModel):
    phone: str
    password: str

# JWT Token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
