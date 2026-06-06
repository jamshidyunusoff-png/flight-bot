"""
Handlers for the ➕ Add Flight flow (FSM).
"""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.database import add_flight
from app.keyboards import BTN_ADD_FLIGHT, main_menu_keyboard
from app.states import AddFlightStates
from app.utils.formatters import fmt_flight_saved
from app.utils.time_utils import minutes_to_hhmm, parse_time, today_iso

logger = logging.getLogger(__name__)
router = Router(name="add_flight")

# ---------------------------------------------------------------------------
# Step 0 — trigger
# ---------------------------------------------------------------------------

@router.message(F.text == BTN_ADD_FLIGHT)
async def add_flight_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(AddFlightStates.waiting_destination)
    await message.answer(
        "🛬 <b>Destination?</b>\n\nEnter the name of the destination airport or city.",
        reply_markup=main_menu_keyboard(),
    )


# ---------------------------------------------------------------------------
# Step 1 — destination
# ---------------------------------------------------------------------------

@router.message(AddFlightStates.waiting_destination)
async def add_flight_destination(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()

    if not text:
        await message.answer("❗ Destination cannot be empty. Please enter a destination:")
        return

    if len(text) > 100:
        await message.answer("❗ Destination is too long (max 100 characters). Try again:")
        return

    await state.update_data(destination=text)
    await state.set_state(AddFlightStates.waiting_flight_time)
    await message.answer(
        "⏱ <b>Total flight time?</b>\n\n"
        "Format: <code>H:MM</code> or <code>HH:MM</code>\n"
        "Examples: <code>5:45</code>  <code>05:45</code>  <code>0:30</code>  <code>12:05</code>"
    )


# ---------------------------------------------------------------------------
# Step 2 — total flight time
# ---------------------------------------------------------------------------

@router.message(AddFlightStates.waiting_flight_time)
async def add_flight_flight_time(message: Message, state: FSMContext) -> None:
    raw = (message.text or "").strip()
    minutes = parse_time(raw)

    if minutes is None:
        await message.answer(
            "❗ Invalid time format.\n\n"
            "Please use <code>H:MM</code> or <code>HH:MM</code>\n"
            "Examples: <code>5:45</code>  <code>05:45</code>  <code>0:30</code>\n\n"
            "⏱ <b>Total flight time?</b>"
        )
        return

    await state.update_data(flight_minutes=minutes)
    await state.set_state(AddFlightStates.waiting_night_time)
    await message.answer(
        "🌙 <b>Night flight time?</b>\n\n"
        "Format: <code>H:MM</code> or <code>HH:MM</code>\n"
        "Examples: <code>2:15</code>  <code>02:15</code>  <code>0:00</code>\n\n"
        f"(Total flight time: <code>{minutes_to_hhmm(minutes)}</code>)"
    )


# ---------------------------------------------------------------------------
# Step 3 — night time
# ---------------------------------------------------------------------------

@router.message(AddFlightStates.waiting_night_time)
async def add_flight_night_time(message: Message, state: FSMContext) -> None:
    raw = (message.text or "").strip()
    night_minutes = parse_time(raw)

    if night_minutes is None:
        await message.answer(
            "❗ Invalid time format.\n\n"
            "Please use <code>H:MM</code> or <code>HH:MM</code>\n"
            "Examples: <code>2:15</code>  <code>02:15</code>  <code>0:00</code>\n\n"
            "🌙 <b>Night flight time?</b>"
        )
        return

    data = await state.get_data()
    flight_minutes: int = data["flight_minutes"]

    if night_minutes > flight_minutes:
        await message.answer(
            f"❗ Night time (<code>{minutes_to_hhmm(night_minutes)}</code>) "
            f"cannot exceed total flight time "
            f"(<code>{minutes_to_hhmm(flight_minutes)}</code>).\n\n"
            "🌙 <b>Night flight time?</b>"
        )
        return

    # All good — persist
    user_id = message.from_user.id if message.from_user else 0
    try:
        flight = await add_flight(
            user_id=user_id,
            date=today_iso(),
            destination=data["destination"],
            flight_minutes=flight_minutes,
            night_minutes=night_minutes,
        )
    except Exception:
        logger.exception("Failed to save flight for user %s.", user_id)
        await message.answer(
            "⚠️ Sorry, something went wrong saving your flight. Please try again.",
            reply_markup=main_menu_keyboard(),
        )
        await state.clear()
        return

    await state.clear()
    logger.info(
        "Flight saved — user=%s  dest=%s  ft=%d  nt=%d",
        user_id,
        data["destination"],
        flight_minutes,
        night_minutes,
    )
    await message.answer(fmt_flight_saved(flight), reply_markup=main_menu_keyboard())
