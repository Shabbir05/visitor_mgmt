# routes/visitors.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.visitor import VisitorCreate, VisitorResponse
from app.schemas.user import UserOut
from app.database import get_db
from app.utils.dependencies import get_current_user, require_role
from app.services.visitor_service import create_visitor_with_visit
from app.models.user import User, UserRole

router = APIRouter()

# Security creates a visitor
@router.post("/", response_model=VisitorResponse)
def create_visitor(
    visitor: VisitorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("SECURITY"))
):
    """
    Security creates a visitor. Automatically creates a visit in PENDING status.
    """
    try:
        new_visitor, visit = create_visitor_with_visit(
            db=db,
            name=visitor.name,
            phone=visitor.phone,
            visitor_type=visitor.visitor_type,
            resident_id=visitor.resident_id  # Selected by security
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": new_visitor.id,
        "name": new_visitor.name,
        "phone": new_visitor.phone,
        "visitor_type": new_visitor.visitor_type,
        "resident_id": new_visitor.resident_id,
        "visit_id": visit.id
    }

# Fetch all residents (for dropdown)
@router.get("/resident/all", response_model=list[UserOut])
def get_all_residents(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("SECURITY"))
):
    """
    Security can fetch all residents to populate dropdown
    """
    residents = db.query(User).filter(User.role == UserRole.RESIDENT).all()
    return residents
