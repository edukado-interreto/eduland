from http import HTTPStatus
from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from django_rsgi.serve import serve_file

from wagtail.models.pages import Page

from config.utils import Environment


@cache_page(60 * 60 * 24 * 30)
def public(request: HttpRequest, public_file: str):
    if public_file == "robots.txt" and settings.ENVIRONMENT != Environment.PRODUCTION:
        public_file = "no-robots.txt"
    return serve_file(request, path=public_file, document_root=settings.PUBLIC_ROOT)


def serve_upload(
    request: HttpRequest,
    path: str | Path,
    document_root: str | Path | None = None,
    **kwargs,
):
    """Add Cache-Control header to django_rsgi.serve_file response."""
    response = serve_file(request, path, document_root, **kwargs)
    response.headers["Cache-Control"] = "max-age=7776000, public"
    return response


def healthcheck(request: HttpRequest) -> HttpResponse:
    if "exception" in request.GET:
        raise Exception("Raised Exception on purpose to send it to Bugsink")

    try:  # Database check
        Page.objects.values_list("slug")
    except Exception as error:
        print(error)
        return JsonResponse(
            {"status": "error", "error": error},
            status=HTTPStatus.SERVICE_UNAVAILABLE,
        )

    return JsonResponse({"status": "ok"})
