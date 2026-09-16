from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, seed
from .config import get_settings
from .database import Base, SessionLocal, engine
from .routers import bookings, contact, courses, plagiarism, projects, services

settings = get_settings()

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed.run(db)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services.router)
app.include_router(projects.router)
app.include_router(courses.router)
app.include_router(bookings.router)
app.include_router(contact.router)
app.include_router(plagiarism.router)


@app.get("/")
@app.get("/api/health")
def health():
    return {"message": "App is working"}
