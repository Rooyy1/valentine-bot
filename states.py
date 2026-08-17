from aiogram.fsm.state import State, StatesGroup


class Diagnostics(StatesGroup):
    # Для тренировок
    workouts_q1 = State()
    workouts_q2 = State()

    # Для питания
    nutrition_q1 = State()
    nutrition_q2 = State()

    # Для готовой системы
    system_q1 = State()
    system_q2 = State()