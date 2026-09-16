from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=List[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return (
        db.query(models.Project)
        .order_by(models.Project.is_featured.desc(), models.Project.sort_order.asc())
        .all()
    )
