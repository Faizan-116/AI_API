import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class ServiceCategory(str, enum.Enum):
    assignment_help = "assignment_help"
    dissertation_help = "dissertation_help"
    viva_prep = "viva_prep"
    demo_lecture = "demo_lecture"
    one_to_one_course = "one_to_one_course"
    plagiarism_check = "plagiarism_check"
    other = "other"


class PriceType(str, enum.Enum):
    hourly = "hourly"
    fixed = "fixed"
    package = "package"


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    title = Column(String(160), nullable=False)
    short_description = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(ServiceCategory), nullable=False)
    price_type = Column(Enum(PriceType), nullable=False, default=PriceType.hourly)
    price = Column(Float, nullable=False, default=0)
    duration_minutes = Column(Integer, nullable=False, default=60)
    is_active = Column(Boolean, default=True)

    bookings = relationship("Booking", back_populates="service")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(160), nullable=False)
    description = Column(Text, nullable=False)
    tech_stack = Column(String(300), nullable=True)  # comma-separated
    category = Column(String(120), nullable=True)
    image_url = Column(String(500), nullable=True)
    project_url = Column(String(500), nullable=True)
    is_featured = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    title = Column(String(160), nullable=False)
    description = Column(Text, nullable=False)
    level = Column(String(50), nullable=False, default="beginner")
    price = Column(Float, nullable=False, default=0)
    duration_weeks = Column(Integer, nullable=False, default=1)
    is_one_to_one = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    bookings = relationship("Booking", back_populates="course")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(160), nullable=False)
    student_email = Column(String(255), nullable=False, index=True)
    notes = Column(Text, nullable=True)

    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.pending)
    calendar_event_id = Column(String(255), nullable=True)
    meet_link = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    service = relationship("Service", back_populates="bookings")
    course = relationship("Course", back_populates="bookings")


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(160), nullable=False)
    email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class PlagiarismCheckStatus(str, enum.Enum):
    submitted = "submitted"
    processing = "processing"
    complete = "complete"
    failed = "failed"


class PlagiarismCheckRequest(Base):
    __tablename__ = "plagiarism_check_requests"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(160), nullable=False)
    student_email = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    turnitin_submission_id = Column(String(255), nullable=True)
    status = Column(Enum(PlagiarismCheckStatus), default=PlagiarismCheckStatus.submitted)
    similarity_score = Column(Float, nullable=True)
    ai_score = Column(Float, nullable=True)
    report_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
