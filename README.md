# ✈️ Flight Hours Bot

A production-ready Telegram bot for pilots to log flights and calculate monthly totals.

Built with **Python 3.12 + aiogram 3.x + SQLite**.  Deploys in one click to Railway (free tier).

---

## Features

| Button | What it does |
|---|---|
| ➕ Add Flight | FSM wizard — enter destination, total time, night time |
| 📅 This Month | Full report with per-flight rows and totals |
| 📆 Previous Month | Same report for the previous calendar month |
| 🗑 Delete Last Flight | Shows last flight details, asks for confirmation, then deletes |

### Time entry format
- `5:45` → `05:45`  
- `4:05` → `04:05`  
- `0:30` → `00:30`  
- `12:05` → `12:05`  
- Rejects: `5.45`, `545`, `5:99`, `abc`

---

## Project Structure

```
flight_hours_bot/
├── main.py                    # Entry point — bot + dispatcher setup
├── requirements.txt
├── runtime.txt                # Python 3.12 for Railway
├── Procfile                   # Railway start command
├── railway.json               # Railway deployment config
├── .env.example               # Template for environment variables
├── .gitignore
├── README.md
└── app/
    ├── config.py              # Pydantic-settings configuration
    ├── states.py              # FSM state groups
    ├── database/
    │   ├── __init__.py
    │   └── db.py              # aiosqlite CRUD layer
    ├── handlers/
    │   ├── __init__.py        # Router registration
    │   ├── common.py          # /start, /help
    │   ├── add_flight.py      # FSM: Add Flight flow
    │   ├── reports.py         # This Month / Previous Month
    │   └── delete_flight.py   # Delete Last Flight + confirmation
    ├── keyboards/
    │   ├── __init__.py
    │   └── keyboards.py       # Main menu + inline confirm keyboard
    └── utils/
        ├── __init__.py
        ├── time_utils.py      # parse_time, minutes_to_hhmm, date helpers
        └── formatters.py      # Human-readable message builders
```

---

## Database Schema

```sql
CREATE TABLE flights (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,           -- Telegram user ID
    date            TEXT    NOT NULL,           -- ISO-8601: YYYY-MM-DD
    destination     TEXT    NOT NULL,
    flight_minutes  INTEGER NOT NULL,           -- stored as total minutes
    night_minutes   INTEGER NOT NULL
);

CREATE INDEX idx_flights_user_date ON flights (user_id, date);
```

Durations are stored as **integer minutes** and converted to `HH:MM` only for display.

---

## Local Setup

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/flight-hours-bot.git
cd flight-hours-bot
```

### 2. Create a virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a Telegram bot with BotFather

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow the prompts — choose a name and username
4. BotFather will reply with your **Bot Token** (looks like `123456789:ABCdef…`)
5. Optionally, send `/setcommands` and set:
   ```
   start - Start the bot
   help - Show help
   ```

### 5. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:
```dotenv
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
DATABASE_URL=flights.db
```

### 6. Run

```bash
python main.py
```

You should see:
```
2024-06-15 10:00:00 | INFO     | __main__: Starting Flight Hours Bot …
2024-06-15 10:00:00 | INFO     | app.database.db: Database ready at 'flights.db'.
2024-06-15 10:00:00 | INFO     | __main__: Handlers registered.
```

Open Telegram, find your bot, and send `/start`.

---

## Railway Deployment

Railway provides a free tier that is sufficient for a personal bot.

### Step 1 — Create a Railway account

Go to [railway.app](https://railway.app) and sign up (GitHub login recommended).

### Step 2 — Push your code to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/flight-hours-bot.git
git push -u origin main
```

### Step 3 — Create a new Railway project

1. Log in to Railway → **New Project**
2. Choose **Deploy from GitHub repo**
3. Authorise Railway to access your repos
4. Select **flight-hours-bot**

### Step 4 — Add environment variables

In Railway project settings → **Variables** → **New Variable**:

| Key | Value |
|---|---|
| `BOT_TOKEN` | `123456789:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `DATABASE_URL` | `flights.db` |

> **Important:** Never paste the token in plain text anywhere else.

### Step 5 — Deploy

Railway auto-detects `railway.json` and `runtime.txt`.  
Click **Deploy** (or it deploys automatically on push).

Watch the build logs.  When you see:
```
Starting Flight Hours Bot …
Database ready at 'flights.db'.
```
the bot is live. 🎉

### Step 6 — Persistent storage note

Railway's ephemeral filesystem resets on redeploy, which means `flights.db` is wiped.  
For a personal pilot logbook this is usually acceptable (data survives restarts, only redeploys reset it).

For true persistence either:
- **Option A:** Add a [Railway Volume](https://docs.railway.app/reference/volumes) and set `DATABASE_URL=/data/flights.db`
- **Option B:** Migrate to [Turso](https://turso.tech) (free, LibSQL-compatible)

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `BOT_TOKEN` | ✅ | — | Telegram bot token from BotFather |
| `DATABASE_URL` | ❌ | `flights.db` | Path to the SQLite database file |

---

## Running Tests

The project ships without a test suite to keep it lean.  To add tests:

```bash
pip install pytest pytest-asyncio
```

Key units to test: `parse_time`, `minutes_to_hhmm`, `iso_to_display`.

---

## Troubleshooting

### Bot not responding
- Make sure `BOT_TOKEN` is set correctly (no extra spaces)
- Check that only **one instance** of the bot is running (long-polling doesn't allow multiple)

### `ModuleNotFoundError: No module named 'aiogram'`
- Activate your virtual environment: `source .venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

### Database errors on Railway after redeploy
- The default `flights.db` file is ephemeral — see the **Persistent storage** note above

### Time validation rejecting valid input
- Make sure you use a colon `:` not a dot `.`
- Minutes must be 00–59
- Format is `H:MM` or `HH:MM`, not `HHMM`

---

## License

MIT — use freely for personal and commercial projects.
