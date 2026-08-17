"""Логика подбора продукта по ответам диагностики.

Каждая функция принимает коды ответов пользователя (callback_data) и
возвращает ключ продукта из PRODUCTS + персонализированный текст-обоснование.
Именно эти функции превращают вопросы диагностики из декоративных в реально
влияющие на то, что увидит пользователь.
"""
from data.products import PRODUCTS
from data.texts import (
    NUTRITION_GOAL_LABELS,
    NUTRITION_PROBLEM_LABELS,
    ONLINE_GOAL_LABELS,
    ONLINE_PRIORITY_LABELS,
    WORKOUT_GOAL_LABELS,
    WORKOUT_PROBLEM_LABELS,
)

# Какую фичу подсветить в карточке "Онлайн-ведение" в зависимости от того,
# что пользователь назвал самым важным.
ONLINE_HIGHLIGHT_KEYWORDS = {
    "oq2_support": "Поддержка 24/7",
    "oq2_video": "Разбор видео",
    "oq2_program": "Программа тренировок",
}


def recommend_workout(goal_code: str, problem_code: str) -> tuple[str, str]:
    """Тренировки: продукт выбирается по проблеме (что мешает прогрессировать),
    а не по цели — цель используется только в тексте обоснования."""
    routing = {
        "wq2_tech": "gym_training",       # разовая проблема с техникой → разовая тренировка
        "wq2_program": "intro",           # нет системы → нужна готовая программа
        "wq2_progress": "online_coaching",  # нет прогресса → нужен постоянный контроль
    }
    key = routing.get(problem_code, "gym_training")

    goal_text = WORKOUT_GOAL_LABELS.get(goal_code, "")
    problem_text = WORKOUT_PROBLEM_LABELS.get(problem_code, "")
    reason = _reason_intro(goal_text, problem_text) + PRODUCTS[key]["why"]
    return key, reason


def recommend_nutrition(problem_code: str, goal_code: str) -> tuple[str, str]:
    """Питание: продукт выбирается по проблеме — если человек просто не знает,
    что готовить, книги рецептов достаточно; если не понимает КБЖУ или срывается
    на вредное, нужен персональный план с поддержкой."""
    routing = {
        "nq1_meals": "recipes",
        "nq1_kbju": "intro",
        "nq1_junk": "intro",
    }
    key = routing.get(problem_code, "intro")

    problem_text = NUTRITION_PROBLEM_LABELS.get(problem_code, "")
    goal_text = NUTRITION_GOAL_LABELS.get(goal_code, "")
    reason = _reason_intro(goal_text, problem_text) + PRODUCTS[key]["why"]
    return key, reason


def recommend_system(count_code: str) -> tuple[str, str]:
    """Готовая система: один вопрос сразу однозначно определяет тариф."""
    key = "base" if count_code == "12" else "comfort"
    return key, PRODUCTS[key]["why"]


def recommend_online(goal_code: str, priority_code: str) -> tuple[str, str, str | None]:
    """Онлайн-ведение: продукт всегда один (тариф не дробится), но ответы
    персонализируют текст и подсвечивают самую важную для клиента фичу."""
    key = "online_coaching"
    goal_text = ONLINE_GOAL_LABELS.get(goal_code, "")
    priority_text = ONLINE_PRIORITY_LABELS.get(priority_code, "")

    reason = _reason_intro(goal_text, "") + PRODUCTS[key]["why"]
    if priority_text:
        reason += f" Особое внимание уделим тому, что для тебя важнее всего: {priority_text}."

    highlight = ONLINE_HIGHLIGHT_KEYWORDS.get(priority_code)
    return key, reason, highlight


def _reason_intro(goal_text: str, problem_text: str) -> str:
    if goal_text and problem_text:
        return (
            f"Ты отметил, что твоя цель — {goal_text}, а сейчас больше всего "
            f"мешает то, что {problem_text}. "
        )
    if goal_text:
        return f"Ты отметил, что твоя цель — {goal_text}. "
    if problem_text:
        return f"Ты отметил, что сейчас больше всего мешает то, что {problem_text}. "
    return ""
