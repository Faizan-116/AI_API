from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # General
    app_name: str = "Lecturer Portfolio API"
    environment: str = "development"
    frontend_origin: str = "http://localhost:5173"

    # Database
    database_url: str = "sqlite:///./portfolio.db"

    # Working hours used to compute booking availability (24h, server local time)
    booking_day_start_hour: int = 9
    booking_day_end_hour: int = 18
    booking_slot_minutes: int = 30
    booking_lookahead_days: int = 14

    # Google Calendar
    google_calendar_credentials_file: str = "credentials.json"
    google_calendar_token_file: str = "token.json"
    google_calendar_id: str = "primary"

    # Turnitin (TCA - Turnitin Core API)
    turnitin_base_url: str = ""
    turnitin_api_key: str = ""
    turnitin_integration_name: str = "portfolio-site"
    turnitin_integration_version: str = "1.0.0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
