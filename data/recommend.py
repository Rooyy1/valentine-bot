"""Логика рекомендации продукта по ответам диагностики.

Бюджет — главный ограничитель (нет смысла предлагать пакет за 23 000 ₽
человеку, который готов заплатить один раз 1 500 ₽). Внутри бюджетного
диапазона уточняем выбор по формату помощи и текущей проблеме.

Ключи продуктов соответствуют data/products.py:
gym_training, intro, online_coaching, intro_plus_4, intro_plus_12, recipes.
"""

from data.products import PRODUCTS
from data.texts import GOAL_LABELS, PROBLEM_LABELS


def recommend_product(answers: dict) -> tuple[str, str]:
    goal = answers.get("goal")
    problem = answers.get("problem")
    fmt = answers.get("format")
    budget = answers.get("budget")

    if budget == "low":
        key = "recipes" if problem == "nutrition" else "gym_training"
    elif budget == "mid":
        key = "intro"
    elif budget == "high":
        key = "intro_plus_4" if fmt == "inperson" else "online_coaching"
    elif budget == "premium":
        key = "intro_plus_12"
    else:
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
