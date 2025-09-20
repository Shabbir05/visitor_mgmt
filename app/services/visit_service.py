from sqlalchemy.orm import Session
from app.models.visit import Visit, ApprovalStatus
from datetime import datetime

def check_in_visitor(db: Session, visit_id: int):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit or visit.status != ApprovalStatus.APPROVED:
        return None
    visit.check_in = datetime.utcnow()
    db.commit()
    db.refresh(visit)
    return visit

def check_out_visitor(db: Session, visit_id: int):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit or not visit.check_in:
        return None
    visit.check_out = datetime.utcnow()
    db.commit()
    db.refresh(visit)
    return visit

def approve_visit(db: Session, visit_id: int):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit or visit.status != ApprovalStatus.PENDING:
        return None
    visit.status = ApprovalStatus.APPROVED
    db.commit()
    db.refresh(visit)
    return visit

def deny_visit(db: Session, visit_id: int):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit or visit.status != ApprovalStatus.PENDING:
        return None
    visit.status = ApprovalStatus.DENIED
    db.commit()
    db.refresh(visit)
    return visit
