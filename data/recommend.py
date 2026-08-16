"""Простая, но понятная логика рекомендации продукта по ответам диагностики.

Бюджет — главный ограничитель. Внутри бюджетного диапазона уточняем выбор
по формату помощи и текущей проблеме.
"""

from data.products import PRODUCTS
from data.texts import GOAL_LABELS, PROBLEM_LABELS


def recommend_product(answers: dict) -> tuple[str, str]:
    goal = answers.get("goal")
    problem = answers.get("problem")
    fmt = answers.get("format")
    budget = answers.get("budget")

    # Логика основана на бюджете как первичном фильтре
    if budget == "low":
        # До 1 500 ₽ — либо книга, либо разовая тренировка
        key = "recipes" if problem == "nutrition" else "personal_training"
    
    elif budget == "mid":
        # ~5 000 ₽ — только введение (без тренировок)
        key = "introduction"
    
    elif budget == "high":
        # 8 000–11 000 ₽ — онлайн-ведение или пакет «Комфорт»
        key = "comfort" if fmt == "inperson" else "online_coaching"
    
    elif budget == "premium":
        # От 23 000 ₽ — пакет «База»
        key = "base"
    
    else:
        # Дефолтный вариант
        key = "online_coaching"

    reason = _build_reason(key, goal, problem)
    return key, reason


def _build_reason(key: str, goal: str, problem: str) -> str:
    product = PRODUCTS[key]
    goal_text = GOAL_LABELS.get(goal, "")
    problem_text = PROBLEM_LABELS.get(problem, "")

    intro = ""
    if goal_text and problem_text:
        intro = (
            f"Ты отметил, что твоя цель — {goal_text}, а сейчас больше всего "
            f"мешает то, что {problem_text}. "
        )

    return f"{intro}{product['why']}"