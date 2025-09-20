# routes/visits.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.visit import Visit, ApprovalStatus
from app.models.user import User
from app.utils.dependencies import require_role

router = APIRouter()

# Resident fetches all visitors for dashboard
@router.get("/resident/visitors")
def get_visitors_for_resident(
    current_user: User = Depends(require_role("RESIDENT")),
    db: Session = Depends(get_db)
):
    """
    Resident dashboard: fetch all visitors related to this resident
    """
    visits = db.query(Visit).filter(Visit.resident_id == current_user.id).all()

    result = []
    for v in visits:
        visitor = v.visitor
        result.append({
            "id": visitor.id,
            "name": visitor.name,
            "phone": visitor.phone,
            "visitor_type": visitor.visitor_type,
            "status": v.status.value,
            "visit_id": v.id
        })
    return result

# Security fetches all visits
@router.get("/security/visits")
def get_visits_for_security(
    current_user: User = Depends(require_role("SECURITY")),
    db: Session = Depends(get_db)
):
    """
    Security dashboard: fetch all pending/approved visitors
    """
    visits = db.query(Visit).all()

    result = []
    for v in visits:
        visitor = v.visitor
        result.append({
            "id": visitor.id,
            "name": visitor.name,
            "phone": visitor.phone,
            "visitor_type": visitor.visitor_type,
            "status": v.status.value,
            "visit_id": v.id,
            "resident_id": v.resident_id
        })
    return result
