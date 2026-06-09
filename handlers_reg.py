"""
Router registration — replaces the handlers/__init__.py package.
Named handlers_reg.py to avoid shadowing any built-in 'handlers' name.
"""

from __future__ import annotations

from aiogram import Dispatcher

from add_flight import router as add_flight_router
from common import router as common_router
from delete_flight import router as delete_flight_router
from reports import router as reports_router


def register_all_handlers(dp: Dispatcher) -> None:
    dp.include_router(add_flight_router)
    dp.include_router(delete_flight_router)
    dp.include_router(reports_router)
    dp.include_router(common_router)
