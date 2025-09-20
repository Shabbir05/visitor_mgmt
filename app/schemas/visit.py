from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VisitBase(BaseModel):
    visitor_id: int
    security_id: int

class VisitCreate(VisitBase):
    pass

class VisitOut(VisitBase):
    id: int
    check_in: Optional[datetime]
    check_out: Optional[datetime]
    status: str  # pending/approved/denied

    class Config:
        orm_mode = True
