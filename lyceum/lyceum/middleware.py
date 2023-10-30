import re

import django.conf
import django.utils.deprecation


__all__ = []


class ReverseRussianWordsMiddleware(django.utils.deprecation.MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counter = 0

    def __call__(self, request):
        response = self.get_response(request)
        self.request_counter += 1

        if django.conf.settings.ALLOW_REVERSE and self.request_counter == 10:
            self.request_counter = 0
            response.content = self.reverse_russian_words(
                response.content.decode("utf-8"),
            )
            return response

        return response

    def reverse_russian_words(self, s):
        words = re.split(r"(\W+)", s)
        reversed_words = [
            word[::-1]
            if not re.match(r"\W+", word) and self.is_russian_word(word)
            else word
            for word in words
        ]
        reversed_string = "".join(reversed_words)
        return reversed_string

    def is_russian_word(self, word):
        for char in word:
            if char.isalpha() and not 1072 <= ord(char.lower()) <= 1103:
                return False
        return True
