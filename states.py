from aiogram.fsm.state import State, StatesGroup


class Diagnostics(StatesGroup):
    # Тренировки (2 вопроса: цель влияет на текст, проблема — на выбор продукта)
    workout_q1 = State()
    workout_q2 = State()

    # Питание (2 вопроса: проблема влияет на выбор продукта, цель — на текст)
    nutrition_q1 = State()
    nutrition_q2 = State()

    # Готовая система (1 вопрос — сразу и однозначно определяет тариф)
    system_q1 = State()

    # Онлайн-ведение (2 вопроса: продукт один, но ответы персонализируют текст)
    online_q1 = State()
    online_q2 = State()
