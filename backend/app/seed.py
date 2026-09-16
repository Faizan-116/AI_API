"""Seeds placeholder services/projects/courses on first run so the site
has content to render before real content is provided. Safe to re-run:
it only inserts rows when the relevant tables are empty.

To replace with real content later, edit the lists below (or add an
admin UI) and re-run, or edit rows directly in the database.
"""

from sqlalchemy.orm import Session

from . import models


def run(db: Session) -> None:
    if db.query(models.Service).count() == 0:
        db.add_all(
            [
                models.Service(
                    slug="assignment-help",
                    title="Assignment Help",
                    short_description="One-to-one guidance to plan, structure, and complete assignments.",
                    description=(
                        "Placeholder description: replace with details of how you help students "
                        "understand requirements, structure their work, and improve quality before "
                        "submission."
                    ),
                    category=models.ServiceCategory.assignment_help,
                    price_type=models.PriceType.hourly,
                    price=25,
                    duration_minutes=60,
                ),
                models.Service(
                    slug="dissertation-support",
                    title="Dissertation & Project Support",
                    short_description="Guidance across proposal, literature review, methodology, and writing.",
                    description="Placeholder description: replace with your dissertation supervision offering.",
                    category=models.ServiceCategory.dissertation_help,
                    price_type=models.PriceType.package,
                    price=150,
                    duration_minutes=60,
                ),
                models.Service(
                    slug="viva-preparation",
                    title="Viva Preparation",
                    short_description="Mock viva sessions and Q&A practice before your real defence.",
                    description="Placeholder description: replace with your viva prep offering.",
                    category=models.ServiceCategory.viva_prep,
                    price_type=models.PriceType.fixed,
                    price=40,
                    duration_minutes=45,
                ),
                models.Service(
                    slug="demo-lecture",
                    title="Free Demo Lecture",
                    short_description="A short taster session so you can see the teaching style before booking a course.",
                    description="Placeholder description: replace with details of what the demo covers.",
                    category=models.ServiceCategory.demo_lecture,
                    price_type=models.PriceType.fixed,
                    price=0,
                    duration_minutes=30,
                ),
                models.Service(
                    slug="plagiarism-ai-check",
                    title="Plagiarism & AI Content Check (Turnitin)",
                    short_description="Submit your document for a similarity and AI-writing report via Turnitin.",
                    description="Placeholder description: replace with your plagiarism/AI-check offering and turnaround time.",
                    category=models.ServiceCategory.plagiarism_check,
                    price_type=models.PriceType.fixed,
                    price=10,
                    duration_minutes=15,
                ),
            ]
        )

    if db.query(models.Course).count() == 0:
        db.add_all(
            [
                models.Course(
                    slug="one-to-one-programming-fundamentals",
                    title="One-to-One: Programming Fundamentals",
                    description="Placeholder description: replace with your course curriculum and outcomes.",
                    level="beginner",
                    price=200,
                    duration_weeks=4,
                    is_one_to_one=True,
                ),
                models.Course(
                    slug="one-to-one-research-methods",
                    title="One-to-One: Research Methods for Dissertations",
                    description="Placeholder description: replace with your course curriculum and outcomes.",
                    level="intermediate",
                    price=250,
                    duration_weeks=4,
                    is_one_to_one=True,
                ),
            ]
        )

    if db.query(models.Project).count() == 0:
        db.add_all(
            [
                models.Project(
                    title="Placeholder Project One",
                    description="Replace with a real project: what it does, your role, and the outcome.",
                    tech_stack="Python, FastAPI, PostgreSQL",
                    category="Research",
                    is_featured=True,
                    sort_order=1,
                ),
                models.Project(
                    title="Placeholder Project Two",
                    description="Replace with a real project: what it does, your role, and the outcome.",
                    tech_stack="React, TypeScript",
                    category="Teaching Tool",
                    is_featured=True,
                    sort_order=2,
                ),
                models.Project(
                    title="Placeholder Project Three",
                    description="Replace with a real project: what it does, your role, and the outcome.",
                    tech_stack="Data Analysis",
                    category="Publication",
                    is_featured=False,
                    sort_order=3,
                ),
            ]
        )

    db.commit()
