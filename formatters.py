"""
Message formatting helpers — build human-readable bot replies.
"""

from __future__ import annotations

from app.database.db import Flight
from app.utils.time_utils import (
    SHORT_MONTH,
    iso_to_display,
    minutes_to_hhmm,
    month_label,
)


def fmt_flight_saved(flight: Flight) -> str:
    """Confirmation message after a flight is saved."""
    return (
        "✅ <b>Flight saved</b>\n\n"
        f"📅 Date: {iso_to_display(flight.date)}\n"
        f"🛬 Destination: {flight.destination}\n"
        f"⏱ Flight Time: {minutes_to_hhmm(flight.flight_minutes)}\n"
        f"🌙 Night Time: {minutes_to_hhmm(flight.night_minutes)}"
    )


def fmt_flight_deleted(flight: Flight) -> str:
    """Confirmation message after a flight is deleted."""
    return (
        "🗑 <b>Flight deleted</b>\n\n"
        f"📅 Date: {iso_to_display(flight.date)}\n"
        f"🛬 Destination: {flight.destination}\n"
        f"⏱ Flight Time: {minutes_to_hhmm(flight.flight_minutes)}\n"
        f"🌙 Night Time: {minutes_to_hhmm(flight.night_minutes)}"
    )


def fmt_month_report(flights: list[Flight], year: int, month: int) -> str:
    """
    Full monthly report.

    Example output:
    📆 June 2024

    01 Jun | Moscow    | 03:20 | 00:00
    05 Jun | Tashkent  | 05:45 | 02:15
    ────────────────────────────────────
    Flights: 2
    Total Flight Time: 09:05
    Total Night Time:  02:15
    """
    header = f"📆 <b>{month_label(year, month)}</b>\n"

    if not flights:
        return header + "\nNo flights recorded this month."

    lines: list[str] = []
    total_flight = 0
    total_night = 0

    for f in flights:
        # Parse DD from ISO date
        day = int(f.date.split("-")[2])
        mon_abbr = SHORT_MONTH[month]
        dest = f.destination[:12].ljust(12)  # pad / truncate for alignment
        ft = minutes_to_hhmm(f.flight_minutes)
        nt = minutes_to_hhmm(f.night_minutes)
        lines.append(f"  {day:02d} {mon_abbr} | {dest} | {ft} | {nt}")
        total_flight += f.flight_minutes
        total_night += f.night_minutes

    separator = "  " + "─" * 42
    summary = (
        f"\n  Flights: {len(flights)}\n"
        f"  Total Flight Time: {minutes_to_hhmm(total_flight)}\n"
        f"  Total Night Time:  {minutes_to_hhmm(total_night)}"
    )

    return header + "\n<pre>" + "\n".join(lines) + "\n" + separator + summary + "</pre>"


def fmt_delete_confirm(flight: Flight) -> str:
    """Ask the user to confirm deletion, showing the flight details."""
    return (
        "⚠️ <b>Delete last flight?</b>\n\n"
        f"📅 {iso_to_display(flight.date)}\n"
        f"🛬 {flight.destination}\n"
        f"⏱ {minutes_to_hhmm(flight.flight_minutes)}"
        f"  🌙 {minutes_to_hhmm(flight.night_minutes)}"
    )
