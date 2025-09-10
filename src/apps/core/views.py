from django.core.files.storage import storages  # type: ignore reportAttributeAccessIssue
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page


@cache_page(60 * 60 * 24 * 30)
def favicon(request: HttpRequest):
    return redirect(storages["staticfiles"].url("favicon.ico"), permanent=True)


def home_page(request: HttpRequest):
    return render(request, "home.html")
