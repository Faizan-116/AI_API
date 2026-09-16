from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("", response_model=List[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).filter(models.Course.is_active.is_(True)).all()


@router.get("/{slug}", response_model=schemas.CourseOut)
def get_course(slug: str, db: Session = Depends(get_db)):
    from fastapi import HTTPException

    course = db.query(models.Course).filter(models.Course.slug == slug).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
