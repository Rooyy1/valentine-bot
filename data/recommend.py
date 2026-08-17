from data.products import PRODUCTS
from data.texts import GOAL_LABELS, PROBLEM_LABELS


def recommend_product(answers: dict) -> tuple[str, str]:
    fmt = answers.get("format")

    if fmt == "onetime":
        key = "gym_training"
    elif fmt == "selfmade":
        key = "intro"
    elif fmt == "online":
        key = "online_coaching"
    elif fmt == "inperson":
        key = "comfort"   # по умолчанию Комфорт, если нужна База — меняй здесь
    else:
        key = "online_coaching"

    reason = _build_reason(key, answers.get("goal"), answers.get("problem"))
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