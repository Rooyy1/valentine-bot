from aiogram.fsm.state import State, StatesGroup

class Diagnostics(StatesGroup):
    # Тренировки (2 вопроса)
    workout_q1 = State()
    workout_q2 = State()

    # Питание (2 вопроса)
    nutrition_q1 = State()
    nutrition_q2 = State()

    # Готовая система (Питание+Тренировки) (2 вопроса)
    system_q1 = State()
    system_q2 = State()

    # Онлайн-ведение (отдельный сценарий, если нужно)
    online_q1 = State()
    online_q2 = State()