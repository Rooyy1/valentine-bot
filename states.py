from aiogram.fsm.state import State, StatesGroup


class Diagnostics(StatesGroup):
    goal = State()
    problem = State()
    format = State()