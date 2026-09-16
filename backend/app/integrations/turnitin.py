"""Turnitin Core API (TCA) client.

Requires a Turnitin Core API integration agreement. Set TURNITIN_BASE_URL
(e.g. https://your-tenant.turnitin.com) and TURNITIN_API_KEY in the
backend's .env file. Until those are set, calls raise
TurnitinNotConfigured so the rest of the site keeps working.

Docs: https://developers.turnitin.com/docs/tca
"""

from __future__ import annotations

import uuid
from typing import Optional

import httpx

from ..config import get_settings


class TurnitinNotConfigured(RuntimeError):
    pass


def _client() -> httpx.Client:
    settings = get_settings()
    if not settings.turnitin_base_url or not settings.turnitin_api_key:
        raise TurnitinNotConfigured(
            "Turnitin API credentials are not set. Add TURNITIN_BASE_URL and "
            "TURNITIN_API_KEY to backend/.env."
        )
    return httpx.Client(
        base_url=settings.turnitin_base_url,
        headers={
            "Authorization": f"Bearer {settings.turnitin_api_key}",
            "X-Turnitin-Integration-Name": settings.turnitin_integration_name,
            "X-Turnitin-Integration-Version": settings.turnitin_integration_version,
        },
        timeout=30.0,
    )


def submit_document(*, owner_email: str, title: str, file_bytes: bytes, file_name: str) -> str:
    """Create a submission, upload the file, and return the submission id."""
    with _client() as client:
        create_resp = client.post(
            "/api/v1/submissions",
            json={
                "owner": owner_email,
                "title": title,
                "submitter": owner_email,
                "eula": {"accepted": True},
            },
        )
        create_resp.raise_for_status()
        submission_id = create_resp.json()["id"]

        upload_resp = client.put(
            f"/api/v1/submissions/{submission_id}/original",
            headers={
                "Content-Type": "application/octet-stream",
                "Content-Disposition": f'inline; filename="{file_name}"',
            },
            content=file_bytes,
        )
        upload_resp.raise_for_status()

        client.put(
            f"/api/v1/submissions/{submission_id}/similarity",
            json={
                "generation_settings": {
                    "search_repositories": [
                        "INTERNET",
                        "SUBMITTED_WORK",
                        "PUBLICATION",
                    ],
                    "auto_exclude_self_matching_scope": "ALL",
                }
            },
        )

        return submission_id


def get_similarity_report(submission_id: str) -> Optional[dict]:
    with _client() as client:
        resp = client.get(f"/api/v1/submissions/{submission_id}/similarity")
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()


def get_ai_writing_report(submission_id: str) -> Optional[dict]:
    with _client() as client:
        resp = client.get(f"/api/v1/submissions/{submission_id}/ai-writing-report")
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()


def new_idempotent_title(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"
