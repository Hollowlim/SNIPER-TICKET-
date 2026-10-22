# YENG TICKET SNIPER — Stage 1

Responsive Next.js / TypeScript / Tailwind dashboard, FastAPI API, SQLAlchemy and SQLite. All events, prices, dates, and categories are fictional mock data. No BookMyShow requests, live inventory, reservations, automated payments, Telegram connection or booking transfer are implemented in Stage 1.

## Open in Visual Studio Code on Windows

Install Python 3.11+ and Node.js 22 LTS with npm. Clone this repository, then use **File → Open Folder** in VS Code to open `SNIPER-TICKET-` (the folder containing this README).

In VS Code choose **Terminal → New Terminal**. These commands use PowerShell; no virtual environment activation or execution policy change is needed.

First terminal — backend:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Second terminal — frontend:

```powershell
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000` on your PC. API documentation is at `http://127.0.0.1:8000/docs`. Keep both terminals running; Ctrl+C stops each service. After the first setup, you can also use **Terminal → Run Task → Backend (Windows)** and **Frontend**.

If a lockfile has not yet been generated, run `npm install` instead of `npm ci` on the first install. Commit the resulting package-lock.json for repeatable future installations.

## Stage 1 functionality

- Search by event title or venue, filter by event type, sort by date or descending sample price.
- Open event detail dialogs with example categories, source, freshness and explicit unknown availability.
- Start/stop watching using hearts or the event dialog; selections persist in SQLite across refreshes and restarts.
- Watchlist view, responsive navigation, empty/loading/error states and API retry.
- Device preference stored in browser local storage. Telegram, booking history and logs clearly disclose their Stage 1 limits.
- Mock event dates are demonstration performance dates. No sale countdown is fabricated.

SQLite `backend/yeng.db` is created and seeded once at API startup. Do not delete it if you want to retain the local watchlist. This is a single-user local application, not a publicly deployable multi-user service.

## Tests and build

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
cd ..\frontend
npm run typecheck
npm run build
```

Tests use an isolated temporary SQLite database. They exercise event filtering, missing events, category uncertainty, health and persistent watchlist operations.

## Linux / cloud

```bash
cd backend
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
# second terminal, from the repository root:
cd frontend
npm ci
npm run dev
```

The frontend proxies `/api/*` to `http://127.0.0.1:8000`. Set `API_BASE_URL` on the Next.js server to override it. No frontend credential is needed.

## PostgreSQL migration path

The ORM reads `DATABASE_URL`; SQLite is the default. For PostgreSQL, install the `psycopg` SQLAlchemy driver, set `DATABASE_URL=postgresql+psycopg://...` securely, and introduce reviewed Alembic migrations before moving existing data. `create_all` creates missing tables but does not migrate schema or copy data. A PostgreSQL migration has not been run in Stage 1.

## Later stages

2. Authorized event discovery, update deduplication, scheduler, Telegram connection and alerts.
3. Per-event preferences, quantity/max-price/fallback validation and verified availability only where permitted.
4. Official booking handoff providers, supported status transitions, browser session continuity and manual payment.

No live integration is implied by the mock adapter. Do not bypass queues, CAPTCHA, verification, purchase limits or platform restrictions. Never store payment details or transfer raw session cookies.
