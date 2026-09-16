# Portfolio & Academic Mentoring Site

A portfolio + services site for a university lecturer working as a
freelance academic mentor: showcases projects and skills, lists paid
services (assignment help, dissertation support, viva prep, demo
lectures, one-to-one courses, plagiarism/AI checks), and lets students
book real appointments against live Google Calendar availability.

## Structure

- `backend/` — FastAPI app (services, courses, projects, bookings,
  contact, plagiarism-check endpoints), SQLite by default.
- `frontend/` — React (Vite) site styled with Tailwind.

## Running locally

**Backend**

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server proxies `/api` to `http://localhost:8000`.

## Editing content

Edit `frontend/src/content.js` for your bio, credentials, and skills.
Edit the seed data in `backend/app/seed.py` for services, courses, and
projects (or edit rows directly in the database once it's running).

## Connecting Google Calendar (live booking availability)

1. In Google Cloud Console, create a project and enable the "Google
   Calendar API".
2. Create an OAuth 2.0 Client ID (Desktop app), download it as
   `backend/credentials.json`.
3. From `backend/`, run:
   ```bash
   python scripts/generate_google_token.py
   ```
   Sign in once in the browser window that opens — this saves
   `backend/token.json`, which the backend then uses (and refreshes
   automatically) for all future requests.
4. Set `GOOGLE_CALENDAR_ID` in `.env` if you don't want to use your
   primary calendar.

Until this is set up, `/api/bookings/availability` returns a 503 and
the frontend shows "Google Calendar may not be connected yet".

## Connecting Turnitin (plagiarism & AI-writing checks)

Requires a Turnitin Core API (TCA) integration agreement. Set
`TURNITIN_BASE_URL` and `TURNITIN_API_KEY` in `backend/.env`. Until
set, `/api/plagiarism-check` returns a 503 and the frontend shows a
matching message.

## Deploying

The root `Procfile` runs the backend with gunicorn. Deploy the
frontend separately (e.g. as a static build via `npm run build`) and
set `FRONTEND_ORIGIN` in the backend's environment to its URL for CORS.
