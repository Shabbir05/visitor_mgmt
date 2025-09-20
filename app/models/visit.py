from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

# Approval status enum
class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"

class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=False)
    resident_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    security_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    check_in = Column(DateTime, nullable=True)
    check_out = Column(DateTime, nullable=True)
    status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING, nullable=False)

    # Relationships
    visitor = relationship("Visitor", back_populates="visits")
    resident = relationship("User", foreign_keys=[resident_id])
