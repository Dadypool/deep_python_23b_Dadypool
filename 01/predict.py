"Homework 1.1 with SomeModel and predict function"


class SomeModel:  # pylint: disable=R0903
    """SomeMode used for prediction
    Implementation doesn't matter"""

    def predict(self, message: str) -> float:
        "Predicts messages's mood"


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    "Predicts message's mood"

    res = model.predict(message)
    if res > good_thresholds:
        return "отл"
    if res >= bad_thresholds:
        return "норм"
    return "неуд"
