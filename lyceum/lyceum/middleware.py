import re

import django.conf
import django.contrib.auth.models
import django.utils.deprecation

import users.models


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
            response.content = self._reverse_russian_words(
                response.content.decode("utf-8"),
            )
            return response

        return response

    @staticmethod
    def _reverse_russian_words(s):
        russian_words_pattern = re.compile(r"^\b[а-яА-яЁё]+\b$")
        words = re.findall(r"\w+|\w+", s)
        new_words = []
        for word in words:
            if re.fullmatch(russian_words_pattern, word):
                reversed_word = word[::-1]
                new_words.append(reversed_word)
            else:
                new_words.append(word)
        pattern = re.compile(r"\b(" + "|".join(map(re.escape, words)) + r")\b")
        return pattern.sub(lambda x: new_words.pop(0), s)


class ProxyUserMiddleware(django.utils.deprecation.MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.model = users.models.ProxyUser

    def __call__(self, request):
        try:
            proxy_user = users.models.ProxyUser.objects.get(
                pk=request.user.pk,
            )
            request.user = proxy_user
        except users.models.ProxyUser.DoesNotExist:
            pass

        response = self.get_response(request)

        return response
