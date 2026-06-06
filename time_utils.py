"""
Utility functions for time parsing, formatting, and date arithmetic.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Matches H:MM, HH:MM  (no leading-zero requirement on hours)
_TIME_RE = re.compile(r"^(\d{1,3}):([0-5]\d)$")

MONTH_NAMES = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

SHORT_MONTH = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
}


# ---------------------------------------------------------------------------
# Time helpers
# ---------------------------------------------------------------------------

def parse_time(raw: str) -> Optional[int]:
    """
    Parse a time string like ``5:45`` or ``05:45`` into total minutes.

    Returns ``None`` when the input is invalid.
    Accepts H:MM or HH:MM notation.  Rejects dots, plain integers, and
    minutes ≥ 60.
    """
    text = raw.strip()
    m = _TIME_RE.match(text)
    if not m:
        return None
    hours = int(m.group(1))
    minutes = int(m.group(2))
    return hours * 60 + minutes


def minutes_to_hhmm(total_minutes: int) -> str:
    """
    Convert an integer number of minutes to ``HH:MM`` string.

    Example: ``325 → "05:25"``
    """
    if total_minutes < 0:
        total_minutes = 0
    h, m = divmod(total_minutes, 60)
    return f"{h:02d}:{m:02d}"


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

def today_iso() -> str:
    """Return today's date as an ISO-8601 string (``YYYY-MM-DD``)."""
    return date.today().isoformat()


def current_year_month() -> tuple[int, int]:
    """Return ``(year, month)`` for today."""
    today = date.today()
    return today.year, today.month


def previous_year_month() -> tuple[int, int]:
    """Return ``(year, month)`` for the previous calendar month."""
    today = date.today()
    if today.month == 1:
        return today.year - 1, 12
    return today.year, today.month - 1


def iso_to_display(iso_date: str) -> str:
    """
    Convert ``YYYY-MM-DD`` to ``DD Mon YYYY``.

    Example: ``"2024-06-15"`` → ``"15 Jun 2024"``
    """
    try:
        d = datetime.strptime(iso_date, "%Y-%m-%d").date()
        return f"{d.day:02d} {SHORT_MONTH[d.month]} {d.year}"
    except ValueError:
        return iso_date


def month_label(year: int, month: int) -> str:
    """Return a human-friendly month label, e.g. ``"June 2024"``."""
    return f"{MONTH_NAMES[month]} {year}"
