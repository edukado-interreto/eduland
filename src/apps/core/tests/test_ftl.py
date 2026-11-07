from pathlib import Path

from django.conf import settings

import pytest
from fluent_compiler.bundle import FluentBundle

LOCALES_DIR = Path(__file__).parents[1] / "locales"
LOCALES = [code for code, _ in settings.LANGUAGES]


def bundle(locale: str) -> FluentBundle:
    return FluentBundle.from_files(locale, [LOCALES_DIR / locale / "core/main.ftl"])


def message_ids(locale: str) -> set[str]:
    with open(LOCALES_DIR / locale / "core/main.ftl") as ftl:
        return {line.split(" =")[0] for line in ftl if line[:1].isalpha()}


def test_all_locales_have_a_file():
    assert sorted(p.name for p in LOCALES_DIR.iterdir()) == sorted(LOCALES)


@pytest.mark.parametrize("locale", LOCALES)
def test_same_messages_as_english(locale):
    assert message_ids(locale) == message_ids("en")


@pytest.mark.parametrize("locale", LOCALES)
def test_messages_compile(locale):
    assert bundle(locale).check_messages() == []


@pytest.mark.parametrize("locale", LOCALES)
@pytest.mark.parametrize("count", [0, 1, 2, 5, 21])
def test_messages_format(locale, count):
    ftl = bundle(locale)
    for message_id in message_ids("en"):
        text, errors = ftl.format(message_id, {"count": count})
        assert errors == [], message_id
        assert text, message_id
