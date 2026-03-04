from random import choices
from string import ascii_lowercase, digits
from typing import cast

__all__ = ["CHARS", "field_panels", "get_url", "long_id"]

CHARS = digits + ascii_lowercase.replace("i", "").replace("o", "")


def long_id(length=7):
    return "".join(choices(CHARS, k=length))


def get_url(request):
    return f"{request.scheme}://{request.get_host()}{request.path}"


def field_panels(panels):
    from wagtail.admin.panels import Panel
    from wagtail.models import Page

    Panels = list[Panel | str]

    return cast(Panels, Page.content_panels) + panels
