from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# Visitor types
class VisitorType(str, enum.Enum):
    TEMPORARY = "temporary"
    RECURRING = "recurring"

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    visitor_type = Column(Enum(VisitorType), nullable=False)

    # The resident who registered this visitor
    resident_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    resident = relationship("User", backref="visitors")
    visits = relationship("Visit", back_populates="visitor")
