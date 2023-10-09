"Homework 1.1 with SomeModel and predict function"


class SomeModel:  # pylint: disable=R0903
    """SomeMode used for prediction
    Implementation doesn't matter"""

    def predict(self, message: str) -> float:
        "Predicts messages's mood"

        return round(
            len([i for i in message if i.lower() in "ауеыоэяию"]) / len(message), 2
        )


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
    if bad_thresholds <= res <= good_thresholds:
        return "норм"
    return "неуд"
