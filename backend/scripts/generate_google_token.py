"""One-time interactive script to authorize this app against your Google
account and save a refreshable token.json for the backend to use.

Usage (from backend/):
    python scripts/generate_google_token.py

Requires credentials.json (OAuth 2.0 Desktop app client) downloaded from
Google Cloud Console to be present in backend/ (or set
GOOGLE_CALENDAR_CREDENTIALS_FILE to its path).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from google_auth_oauthlib.flow import InstalledAppFlow  # noqa: E402

from app.config import get_settings  # noqa: E402
from app.integrations.google_calendar import SCOPES  # noqa: E402


def main() -> None:
    settings = get_settings()
    flow = InstalledAppFlow.from_client_secrets_file(settings.google_calendar_credentials_file, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(settings.google_calendar_token_file, "w") as f:
        f.write(creds.to_json())
    print(f"Saved token to {settings.google_calendar_token_file}")


if __name__ == "__main__":
    main()
