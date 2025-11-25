from random import choices
from string import ascii_lowercase, digits

CHARS = digits + ascii_lowercase.replace("i", "").replace("o", "")


def long_id(length=7):
    return "".join(choices(CHARS, k=length))


def get_url(request):
    return f"{request.scheme}://{request.get_host()}{request.path}"
