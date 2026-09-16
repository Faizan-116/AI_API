from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..integrations import turnitin
from ..integrations.turnitin import TurnitinNotConfigured

router = APIRouter(prefix="/api/plagiarism-check", tags=["plagiarism-check"])


@router.post("", response_model=schemas.PlagiarismCheckOut, status_code=201)
async def submit_plagiarism_check(
    student_name: str = Form(...),
    student_email: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    file_bytes = await file.read()

    request = models.PlagiarismCheckRequest(
        student_name=student_name,
        student_email=student_email,
        file_name=file.filename,
        status=models.PlagiarismCheckStatus.submitted,
    )
    db.add(request)
    db.commit()
    db.refresh(request)

    try:
        submission_id = turnitin.submit_document(
            owner_email=student_email,
            title=turnitin.new_idempotent_title(file.filename or "submission"),
            file_bytes=file_bytes,
            file_name=file.filename or "submission",
        )
        request.turnitin_submission_id = submission_id
        request.status = models.PlagiarismCheckStatus.processing
        db.commit()
        db.refresh(request)
    except TurnitinNotConfigured as exc:
        request.status = models.PlagiarismCheckStatus.failed
        db.commit()
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return request


@router.get("/{request_id}", response_model=schemas.PlagiarismCheckOut)
def get_plagiarism_check(request_id: int, db: Session = Depends(get_db)):
    request = db.get(models.PlagiarismCheckRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if request.turnitin_submission_id and request.status == models.PlagiarismCheckStatus.processing:
        similarity = turnitin.get_similarity_report(request.turnitin_submission_id)
        if similarity and similarity.get("status") == "COMPLETE":
            request.similarity_score = similarity.get("overall_match_percentage")
            ai_report = turnitin.get_ai_writing_report(request.turnitin_submission_id)
            if ai_report:
                request.ai_score = ai_report.get("ai_writing_overall_match_percentage")
            request.status = models.PlagiarismCheckStatus.complete
            db.commit()
            db.refresh(request)

    return request
