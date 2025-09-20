from pydantic import BaseModel

class VisitorCreate(BaseModel):
    name: str
    phone: str
    visitor_type: str  # temporary or recurring
    resident_id: int   # ❗ required by Security

class VisitorResponse(BaseModel):
    id: int
    name: str
    phone: str
    visitor_type: str
    resident_id: int

    class Config:
        orm_mode = True
