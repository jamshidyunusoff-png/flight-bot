"""
FSM state definitions.
"""

from aiogram.fsm.state import State, StatesGroup


class AddFlightStates(StatesGroup):
    waiting_destination = State()
    waiting_flight_time = State()
    waiting_night_time = State()


class DeleteFlightStates(StatesGroup):
    waiting_confirm = State()
