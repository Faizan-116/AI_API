from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from .models import BookingStatus, PlagiarismCheckStatus, PriceType, ServiceCategory


class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    short_description: str
    description: str
    category: ServiceCategory
    price_type: PriceType
    price: float
    duration_minutes: int
    is_active: bool


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    tech_stack: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    project_url: Optional[str] = None
    is_featured: bool


class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    description: str
    level: str
    price: float
    duration_weeks: int
    is_one_to_one: bool
    is_active: bool


class AvailabilitySlot(BaseModel):
    start: datetime
    end: datetime


class BookingCreate(BaseModel):
    student_name: str
    student_email: EmailStr
    notes: Optional[str] = None
    service_id: Optional[int] = None
    course_id: Optional[int] = None
    start_time: datetime
    end_time: datetime


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_name: str
    student_email: EmailStr
    notes: Optional[str] = None
    service_id: Optional[int] = None
    course_id: Optional[int] = None
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    meet_link: Optional[str] = None
    created_at: datetime


class ContactMessageCreate(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str


class ContactMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str
    created_at: datetime


class PlagiarismCheckOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_name: str
    student_email: EmailStr
    file_name: str
    turnitin_submission_id: Optional[str] = None
    status: PlagiarismCheckStatus
    similarity_score: Optional[float] = None
    ai_score: Optional[float] = None
    report_url: Optional[str] = None
    created_at: datetime
