from pathlib import Path
from http import HTTPStatus

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from django_rsgi.serve import serve_file
from wagtail.models.pages import Page


def _get_public_files_re():
    r"""
    Format public files as "favicon\.ico|robots\.txt"
    """
    public_files = (f.name for f in settings.PUBLIC_ROOT.glob("*.*"))
    return r"|".join(f.replace(".", r"\.") for f in public_files)


PUBLIC_FILES_URL = rf"^(?P<filename>{_get_public_files_re()})$"


@cache_page(60 * 60 * 24 * 30)
def public(request: HttpRequest, filename: str):
    return serve_file(request, path=filename, document_root=settings.PUBLIC_ROOT)


def robots(request: HttpRequest):
    path = "robots.txt" if settings.ENVIRONMENT == "production" else "no-robots.txt"
    return serve_file(request, path, document_root=settings.PUBLIC_ROOT)


def serve_upload(
    request: HttpRequest,
    path: str | Path,
    document_root: str | Path | None = None,
    **kwargs,
):
    "Add Cache-Control header to django_rsgi.serve_file response."
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
