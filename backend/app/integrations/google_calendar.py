"""Google Calendar integration used to compute live availability and create
booking events.

Setup (one-time, done by the site owner, not per-student):
  1. Create a Google Cloud project, enable the "Google Calendar API".
  2. Create an OAuth 2.0 Client ID (Desktop app) and download it as
     credentials.json into the backend/ folder (path configurable via
     GOOGLE_CALENDAR_CREDENTIALS_FILE).
  3. Run `python scripts/generate_google_token.py` once, sign in, and it
     will save a refreshable token.json (path configurable via
     GOOGLE_CALENDAR_TOKEN_FILE). After that, this module refreshes the
     token automatically and needs no further interaction.
"""

from __future__ import annotations

import datetime as dt
import os
from typing import List

from ..config import get_settings
from ..schemas import AvailabilitySlot

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendarNotConfigured(RuntimeError):
    pass


def _load_credentials():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    settings = get_settings()
    token_file = settings.google_calendar_token_file

    if not os.path.exists(token_file):
        raise GoogleCalendarNotConfigured(
            "Google Calendar is not connected yet. Run "
            "scripts/generate_google_token.py once to authorize."
        )

    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_file, "w") as f:
            f.write(creds.to_json())
    return creds


def _get_service():
    from googleapiclient.discovery import build

    creds = _load_credentials()
    return build("calendar", "v3", credentials=creds, cache_discovery=False)


def get_available_slots(duration_minutes: int) -> List[AvailabilitySlot]:
    """Return free slots over the next `booking_lookahead_days`, within
    working hours, that are at least `duration_minutes` long and not
    already busy on the configured calendar."""
    settings = get_settings()
    service = _get_service()

    now = dt.datetime.utcnow()
    horizon = now + dt.timedelta(days=settings.booking_lookahead_days)

    freebusy = service.freebusy().query(
        body={
            "timeMin": now.isoformat() + "Z",
            "timeMax": horizon.isoformat() + "Z",
            "items": [{"id": settings.google_calendar_id}],
        }
    ).execute()
    busy_periods = freebusy["calendars"][settings.google_calendar_id]["busy"]
    busy = [
        (
            dt.datetime.fromisoformat(b["start"].replace("Z", "+00:00")),
            dt.datetime.fromisoformat(b["end"].replace("Z", "+00:00")),
        )
        for b in busy_periods
    ]

    slots: List[AvailabilitySlot] = []
    step = dt.timedelta(minutes=settings.booking_slot_minutes)
    duration = dt.timedelta(minutes=duration_minutes)

    day_cursor = now.date()
    end_date = horizon.date()
    while day_cursor <= end_date:
        day_start = dt.datetime.combine(
            day_cursor, dt.time(hour=settings.booking_day_start_hour), tzinfo=dt.timezone.utc
        )
        day_end = dt.datetime.combine(
            day_cursor, dt.time(hour=settings.booking_day_end_hour), tzinfo=dt.timezone.utc
        )
        cursor = max(day_start, now.replace(tzinfo=dt.timezone.utc))
        while cursor + duration <= day_end:
            candidate_end = cursor + duration
            overlaps = any(cursor < b_end and candidate_end > b_start for b_start, b_end in busy)
            if not overlaps:
                slots.append(AvailabilitySlot(start=cursor, end=candidate_end))
            cursor += step
        day_cursor += dt.timedelta(days=1)

    return slots


def create_event(
    *, summary: str, description: str, start: dt.datetime, end: dt.datetime, attendee_email: str
) -> dict:
    """Create a calendar event with a Google Meet link and invite the student."""
    settings = get_settings()
    service = _get_service()

    event_body = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end.isoformat(), "timeZone": "UTC"},
        "attendees": [{"email": attendee_email}],
        "conferenceData": {
            "createRequest": {
                "requestId": f"booking-{start.timestamp()}",
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
            }
        },
    }

    created = service.events().insert(
        calendarId=settings.google_calendar_id,
        body=event_body,
        conferenceDataVersion=1,
        sendUpdates="all",
    ).execute()

    meet_link = None
    for entry_point in created.get("conferenceData", {}).get("entryPoints", []):
        if entry_point.get("entryPointType") == "video":
            meet_link = entry_point.get("uri")
            break

    return {"event_id": created["id"], "meet_link": meet_link}


def cancel_event(event_id: str) -> None:
    settings = get_settings()
    service = _get_service()
    service.events().delete(
        calendarId=settings.google_calendar_id, eventId=event_id, sendUpdates="all"
    ).execute()
