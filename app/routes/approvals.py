from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.visit import Visit, ApprovalStatus
from app.models.user import User
from app.utils.dependencies import require_role

router = APIRouter(prefix="/approvals")

# Approve a visit
@router.post("/approve/{visit_id}")
def approve_visit(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("RESIDENT"))
):
    # Fetch visit by id and ensure it belongs to logged-in resident
    visit = db.query(Visit).filter(
        Visit.id == visit_id,
        Visit.resident_id == current_user.id
    ).first()

    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found for this resident")

    if visit.status != ApprovalStatus.PENDING:
        raise HTTPException(status_code=400, detail=f"Visit already {visit.status.value.lower()}")

    visit.status = ApprovalStatus.APPROVED
    db.commit()
    db.refresh(visit)

    return {"visit_id": visit.id, "status": visit.status.value}

# Deny a visit
@router.post("/deny/{visit_id}")
def deny_visit(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("RESIDENT"))
):
    visit = db.query(Visit).filter(
        Visit.id == visit_id,
        Visit.resident_id == current_user.id
    ).first()

    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found for this resident")

    if visit.status != ApprovalStatus.PENDING:
        raise HTTPException(status_code=400, detail=f"Visit already {visit.status.value.lower()}")

    visit.status = ApprovalStatus.DENIED
    db.commit()
    db.refresh(visit)

    return {"visit_id": visit.id, "status": visit.status.value}
