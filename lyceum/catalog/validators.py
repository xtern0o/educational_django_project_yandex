import re

import django.core.exceptions
import django.utils.deconstruct


__all__ = []


@django.utils.deconstruct.deconstructible
class ValidateMustContain:
    def __init__(self, *words):
        self._words = words

    def __call__(self, text):
        regex = r"\b(?:{})\b".format("|".join(self._words))
        if not re.findall(regex, text, flags=re.IGNORECASE | re.UNICODE):
            raise django.core.exceptions.ValidationError(
                "В тексте должно содержаться хотя бы одно из слов: {}".format(
                    ", ".join(self._words),
                ),
            )
