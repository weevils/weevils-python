import random
import string

_LEX = string.ascii_letters + string.digits


def random_string(length: int = 16) -> str:
    return "".join(random.choice(_LEX) for _ in range(length))
