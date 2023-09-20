class SomeModel:
    def predict(self, message: str) -> float:
        if not message:
            return 0
        vowels = 0
        for ch in message.lower():
            if ch in "ауеыоэяию":
                vowels += 1
        return round(vowels / len(message), 2)

def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    res = model.predict(message)
    if res > good_thresholds:
        return "отл"
    elif bad_thresholds <= res <= good_thresholds:
        return "норм"
    else:
        return "неуд"