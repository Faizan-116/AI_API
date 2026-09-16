from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/services", tags=["services"])


@router.get("", response_model=List[schemas.ServiceOut])
def list_services(db: Session = Depends(get_db)):
    return db.query(models.Service).filter(models.Service.is_active.is_(True)).all()


@router.get("/{slug}", response_model=schemas.ServiceOut)
def get_service(slug: str, db: Session = Depends(get_db)):
    from fastapi import HTTPException

    service = db.query(models.Service).filter(models.Service.slug == slug).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service
