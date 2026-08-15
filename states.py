from aiogram.fsm.state import State, StatesGroup


class Diagnostics(StatesGroup):
    """Шаги короткого диагностического опроса."""

    goal = State()      # цель клиента
    problem = State()   # текущая проблема
    format = State()    # желаемый формат помощи
    budget = State()    # бюджет / готовность к работе
