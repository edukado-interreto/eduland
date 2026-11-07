from django.test import RequestFactory

from apps.core.utils import CHARS, get_url, long_id


def test_chars_without_ambiguous_letters():
    assert "i" not in CHARS
    assert "o" not in CHARS


def test_long_id():
    assert len(long_id()) == 7
    assert len(long_id(length=3)) == 3
    assert set(long_id(length=100)) <= set(CHARS)


def test_get_url():
    request = RequestFactory().get("/en/news/?page=2", HTTP_HOST="127.0.0.1")
    assert get_url(request) == "http://127.0.0.1/en/news/"
