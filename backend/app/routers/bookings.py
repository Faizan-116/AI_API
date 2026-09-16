from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..integrations import google_calendar
from ..integrations.google_calendar import GoogleCalendarNotConfigured

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.get("/availability", response_model=List[schemas.AvailabilitySlot])
def get_availability(
    duration_minutes: int = Query(60, ge=15, le=240),
):
    try:
        return google_calendar.get_available_slots(duration_minutes)
    except GoogleCalendarNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("", response_model=schemas.BookingOut, status_code=201)
def create_booking(payload: schemas.BookingCreate, db: Session = Depends(get_db)):
    service: Optional[models.Service] = None
    course: Optional[models.Course] = None

    if payload.service_id:
        service = db.get(models.Service, payload.service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
    if payload.course_id:
        course = db.get(models.Course, payload.course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
    if not service and not course:
        raise HTTPException(status_code=400, detail="service_id or course_id is required")

    booking = models.Booking(
        student_name=payload.student_name,
        student_email=payload.student_email,
        notes=payload.notes,
        service_id=payload.service_id,
        course_id=payload.course_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        status=models.BookingStatus.pending,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    title = service.title if service else course.title
    try:
        event = google_calendar.create_event(
            summary=f"Session: {title} with {payload.student_name}",
            description=payload.notes or "",
            start=payload.start_time,
            end=payload.end_time,
            attendee_email=payload.student_email,
        )
        booking.calendar_event_id = event["event_id"]
        booking.meet_link = event.get("meet_link")
        booking.status = models.BookingStatus.confirmed
        db.commit()
        db.refresh(booking)
    except GoogleCalendarNotConfigured:
        # Booking is still recorded; the owner confirms manually until
        # Google Calendar is connected.
        pass

    return booking


@router.get("", response_model=List[schemas.BookingOut])
def list_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).order_by(models.Booking.start_time.asc()).all()


@router.post("/{booking_id}/cancel", response_model=schemas.BookingOut)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(models.Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.calendar_event_id:
        try:
            google_calendar.cancel_event(booking.calendar_event_id)
        except GoogleCalendarNotConfigured:
            pass

    booking.status = models.BookingStatus.cancelled
    db.commit()
    db.refresh(booking)
    return booking
