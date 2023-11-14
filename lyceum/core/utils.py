import django.conf
import jwt


__all__ = []


def decode_token(token):
    try:
        data = jwt.decode(
            token,
            django.conf.settings.SECRET_KEY,
            algorithms=["HS256"],
            verify=True,
        )

    except jwt.exceptions.DecodeError:
        return "Неверная ссылка", False

    except jwt.exceptions.ExpiredSignatureError:
        return (
            "Время кода активации истекло."
            f" Прошло более {django.conf.settings.LINK_EXPIRATION} часов"
        ), False

    return data, True
