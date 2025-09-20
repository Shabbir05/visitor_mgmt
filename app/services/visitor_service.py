# services/visitor_service.py
from sqlalchemy.orm import Session
from app.models.visitor import Visitor
from app.models.visit import Visit, ApprovalStatus

def create_visitor_with_visit(db: Session, name: str, phone: str, visitor_type: str, resident_id: int):
    visitor = Visitor(
        name=name,
        phone=phone,
        visitor_type=visitor_type,
        resident_id=resident_id
    )
    db.add(visitor)
    db.commit()
    db.refresh(visitor)

    # Auto-approve recurring visitors
    status = ApprovalStatus.APPROVED if visitor_type == "recurring" else ApprovalStatus.PENDING

    visit = Visit(
        visitor_id=visitor.id,
        resident_id=resident_id,
        status=status,
        check_in=None,
        check_out=None
    )
    db.add(visit)
    db.commit()
    db.refresh(visit)

    return visitor, visit
