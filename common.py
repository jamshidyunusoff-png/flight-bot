"""
Handlers for /start and /help.
"""

from __future__ import annotations

import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards import main_menu_keyboard

logger = logging.getLogger(__name__)
router = Router(name="common")

WELCOME_TEXT = (
    "✈️ <b>Welcome to Flight Hours Bot!</b>\n\n"
    "I help pilots log their flights and generate monthly reports.\n\n"
    "<b>What I can do:</b>\n"
    "  • Save flights with destination, total time, and night time\n"
    "  • Show monthly flight summaries\n"
    "  • Delete the most recent flight\n\n"
    "Use the menu below to get started."
)

HELP_TEXT = (
    "📖 <b>Flight Hours Bot — Help</b>\n\n"
    "<b>➕ Add Flight</b>\n"
    "  Log a new flight.  You will be asked for:\n"
    "  1. Destination\n"
    "  2. Total flight time  (format: H:MM or HH:MM)\n"
    "  3. Night flight time  (format: H:MM or HH:MM)\n\n"
    "<b>📅 This Month</b>\n"
    "  View all flights and totals for the current calendar month.\n\n"
    "<b>📆 Previous Month</b>\n"
    "  View all flights and totals for the previous calendar month.\n\n"
    "<b>🗑 Delete Last Flight</b>\n"
    "  Remove the most recently added flight (with confirmation).\n\n"
    "<b>Time format examples:</b>\n"
    "  <code>5:45</code>  <code>05:45</code>  <code>0:30</code>  <code>12:05</code>"
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    logger.info("User %s started the bot.", message.from_user.id if message.from_user else "unknown")
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=main_menu_keyboard())
