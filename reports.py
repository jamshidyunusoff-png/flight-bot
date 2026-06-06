"""
Handlers for 📅 This Month and 📆 Previous Month reports.
"""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import Message

from app.database import get_flights_for_month
from app.keyboards import BTN_PREV_MONTH, BTN_THIS_MONTH, main_menu_keyboard
from app.utils.formatters import fmt_month_report
from app.utils.time_utils import current_year_month, previous_year_month

logger = logging.getLogger(__name__)
router = Router(name="reports")


@router.message(F.text == BTN_THIS_MONTH)
async def report_this_month(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    year, month = current_year_month()
    flights = await get_flights_for_month(user_id, year, month)
    logger.info("This-month report requested — user=%s  %d/%02d  flights=%d", user_id, year, month, len(flights))
    await message.answer(fmt_month_report(flights, year, month), reply_markup=main_menu_keyboard())


@router.message(F.text == BTN_PREV_MONTH)
async def report_prev_month(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    year, month = previous_year_month()
    flights = await get_flights_for_month(user_id, year, month)
    logger.info("Prev-month report requested — user=%s  %d/%02d  flights=%d", user_id, year, month, len(flights))
    await message.answer(fmt_month_report(flights, year, month), reply_markup=main_menu_keyboard())
