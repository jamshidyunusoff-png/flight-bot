"""
Utility functions for time parsing, formatting, and date arithmetic.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Optional

_TIME_RE = re.compile(r"^(\d{1,3}):([0-5]\d)$")

MONTH_NAMES = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December",
}

SHORT_MONTH = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
}


def parse_time(raw: str) -> Optional[int]:
    text = raw.strip()
    m = _TIME_RE.match(text)
    if not m:
        return None
    return int(m.group(1)) * 60 + int(m.group(2))


def minutes_to_hhmm(total_minutes: int) -> str:
    if total_minutes < 0:
        total_minutes = 0
    h, m = divmod(total_minutes, 60)
    return f"{h:02d}:{m:02d}"


def today_iso() -> str:
    return date.today().isoformat()


def current_year_month() -> tuple[int, int]:
    today = date.today()
    return today.year, today.month


def previous_year_month() -> tuple[int, int]:
    today = date.today()
    if today.month == 1:
        return today.year - 1, 12
    return today.year, today.month - 1


def iso_to_display(iso_date: str) -> str:
    try:
        d = datetime.strptime(iso_date, "%Y-%m-%d").date()
        return f"{d.day:02d} {SHORT_MONTH[d.month]} {d.year}"
    except ValueError:
        return iso_date


def month_label(year: int, month: int) -> str:
    return f"{MONTH_NAMES[month]} {year}"
