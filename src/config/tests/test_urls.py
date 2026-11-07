from django.conf import settings
from django.urls import Resolver404, resolve

import pytest

from apps.core.views import public, serve_upload


@pytest.mark.parametrize(
    "path",
    ["/robots.txt", "/favicon.ico", "/site.webmanifest", "/snippet_thumb/blank.svg"],
)
def test_public_files(path):
    match = resolve(path)
    assert match.func is public
    assert match.kwargs == {"public_file": path.lstrip("/")}


@pytest.mark.parametrize(
    "path", ["/robotsXtxt", "/settings.py", "/snippet_thumb/../settings.py"]
)
def test_not_public_files(path):
    try:
        assert resolve(path).func is not public
    except Resolver404:
        pass


def test_uploads():
    match = resolve("/uploads/documents/comics.pdf")
    assert match.func is serve_upload
    assert match.kwargs == {
        "path": "documents/comics.pdf",
        "document_root": settings.MEDIA_ROOT,
    }
