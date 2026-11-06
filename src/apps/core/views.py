from http import HTTPStatus

from django.conf import settings
from django.db import DatabaseError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from django.views.static import serve

from wagtail.models.pages import Page

from config.utils import Environment


@cache_page(60 * 60 * 24 * 30)
def public(request: HttpRequest, public_file: str):
    if public_file == "robots.txt" and settings.ENVIRONMENT != Environment.PRODUCTION:
        public_file = "no-robots.txt"
    return serve(request, public_file, document_root=settings.PUBLIC_ROOT)


def serve_upload(
    request: HttpRequest, path: str, document_root=None, show_indexes=False
):
    """Add Cache-Control header to django.views.static.serve response."""
    response = serve(request, path, document_root, show_indexes)
    response.headers["Cache-Control"] = "max-age=7776000, public"
    return response


class BugsinkTestError(Exception):
    """Raised on purpose by the healthcheck to test error reporting."""


def healthcheck(request: HttpRequest) -> HttpResponse:
    if "exception" in request.GET:
        raise BugsinkTestError("Raised Exception on purpose to send it to Bugsink")

    try:  # Database check
        Page.objects.exists()
    except DatabaseError as error:
        print(error)
        return JsonResponse(
            {"status": "error", "error": str(error)},
            status=HTTPStatus.SERVICE_UNAVAILABLE,
        )

    return JsonResponse({"status": "ok"})
