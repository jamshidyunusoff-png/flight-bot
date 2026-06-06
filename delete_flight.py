"""
Handler for 🗑 Delete Last Flight — shows confirmation, then deletes.
"""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.database import delete_flight, get_last_flight
from app.keyboards import BTN_DELETE_LAST, confirm_delete_keyboard, main_menu_keyboard
from app.states import DeleteFlightStates
from app.utils.formatters import fmt_delete_confirm, fmt_flight_deleted

logger = logging.getLogger(__name__)
router = Router(name="delete_flight")


# ---------------------------------------------------------------------------
# Step 0 — trigger
# ---------------------------------------------------------------------------

@router.message(F.text == BTN_DELETE_LAST)
async def delete_last_start(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id if message.from_user else 0
    flight = await get_last_flight(user_id)

    if flight is None:
        await message.answer(
            "ℹ️ You have no flights to delete.",
            reply_markup=main_menu_keyboard(),
        )
        return

    await state.set_state(DeleteFlightStates.waiting_confirm)
    await state.update_data(flight_id=flight.id)

    await message.answer(
        fmt_delete_confirm(flight),
        reply_markup=confirm_delete_keyboard(),
    )


# ---------------------------------------------------------------------------
# Step 1a — confirmed
# ---------------------------------------------------------------------------

@router.callback_query(DeleteFlightStates.waiting_confirm, F.data == "delete_yes")
async def delete_confirmed(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    flight_id: int = data["flight_id"]
    user_id = callback.from_user.id if callback.from_user else 0

    # Re-fetch so we can display its details after deletion
    flight = await get_last_flight(user_id)

    deleted = await delete_flight(flight_id)
    await state.clear()

    if callback.message and isinstance(callback.message, Message):
        # Remove inline keyboard from the confirmation message
        await callback.message.edit_reply_markup(reply_markup=None)

    if deleted and flight:
        logger.info("Flight %d deleted by user %s.", flight_id, user_id)
        reply = fmt_flight_deleted(flight)
    else:
        reply = "⚠️ Could not find the flight to delete (it may have already been removed)."

    await callback.answer()
    if callback.message and isinstance(callback.message, Message):
        await callback.message.answer(reply, reply_markup=main_menu_keyboard())


# ---------------------------------------------------------------------------
# Step 1b — cancelled
# ---------------------------------------------------------------------------

@router.callback_query(DeleteFlightStates.waiting_confirm, F.data == "delete_no")
async def delete_cancelled(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer("Deletion cancelled.")
    if callback.message and isinstance(callback.message, Message):
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(
            "❌ Deletion cancelled.", reply_markup=main_menu_keyboard()
        )
