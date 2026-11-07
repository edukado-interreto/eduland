from http import HTTPStatus

from django.conf import settings
from django.db import DatabaseError
from django.http import Http404
from django.test import RequestFactory

from wagtail.models import Page

import pytest

from apps.core.views import BugsinkTestError, serve_upload
from config.utils import Environment


@pytest.mark.django_db
def test_healthcheck(client):
    response = client.get("/healthcheck/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok"}


def test_healthcheck_exception(client):
    with pytest.raises(BugsinkTestError):
        client.get("/healthcheck/?exception")


def test_healthcheck_database_error(client, monkeypatch):
    def exists():
        raise DatabaseError("connection refused")

    monkeypatch.setattr(Page.objects, "exists", exists)
    response = client.get("/healthcheck/")
    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert response.json() == {"status": "error", "error": "connection refused"}


def public_file(name):
    return (settings.PUBLIC_ROOT / name).read_bytes()


def test_robots_txt_outside_production(client):
    response = client.get("/robots.txt")
    assert response.status_code == HTTPStatus.OK
    assert b"".join(response.streaming_content) == public_file("no-robots.txt")


def test_robots_txt_in_production(client, settings):
    settings.ENVIRONMENT = Environment.PRODUCTION
    response = client.get("/robots.txt")
    assert b"".join(response.streaming_content) == public_file("robots.txt")


def test_favicon(client):
    response = client.get("/favicon.ico")
    assert response.status_code == HTTPStatus.OK
    assert b"".join(response.streaming_content) == public_file("favicon.ico")


def test_serve_upload(tmp_path):
    (tmp_path / "comics.pdf").write_bytes(b"%PDF-1.4")
    request = RequestFactory().get("/uploads/comics.pdf")
    response = serve_upload(request, "comics.pdf", document_root=tmp_path)
    assert response.status_code == HTTPStatus.OK
    assert response["Cache-Control"] == "max-age=7776000, public"
    assert response["Content-Type"] == "application/pdf"
    assert b"".join(response.streaming_content) == b"%PDF-1.4"


def test_serve_upload_missing(tmp_path):
    with pytest.raises(Http404):
        serve_upload(RequestFactory().get("/"), "missing.pdf", document_root=tmp_path)
