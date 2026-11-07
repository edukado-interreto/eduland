import pytest

from config.utils import Environment, get_beercss_dir, is_testing, mod


def test_mod():
    assert mod("django", ["db", "contrib.auth", ""]) == [
        "django.db",
        "django.contrib.auth",
        "django",
    ]


@pytest.mark.parametrize(
    ("environment", "display_name", "deployed"),
    [
        (Environment.PRODUCTION, "", True),
        (Environment.STAGING, "TEST", True),
        (Environment.DEV, "DEV", False),
        (Environment.BUILD, "BUILD", False),
        (Environment.TESTING, "TESTING", False),
    ],
)
def test_environment(environment, display_name, deployed):
    assert environment.display_name() == display_name
    assert environment.deployed is deployed


def test_environment_is_attributes():
    assert Environment.DEV.is_dev is True
    assert Environment.DEV.is_production is False
    with pytest.raises(AttributeError):
        Environment.DEV.is_unknown  # noqa: B018


def test_environment_init(monkeypatch):
    config = lambda key, default: {"ENVIRONMENT": "staging"}.get(key, default)

    assert Environment.init(config, debug=False) == Environment.TESTING

    monkeypatch.setattr("config.utils.is_testing", lambda: False)
    assert Environment.init(config, debug=True) == Environment.DEV
    assert Environment.init(config, debug=False) == Environment.STAGING
    assert Environment.init(lambda k, d: d, debug=False) == Environment.PRODUCTION


def test_is_testing():
    assert is_testing()


def test_get_beercss_dir(tmp_path):
    (tmp_path / "beercss-4.0.16").mkdir()
    assert get_beercss_dir(tmp_path) == "beercss-4.0.16"


def test_get_beercss_dir_missing(tmp_path):
    with pytest.raises(IndexError, match="BeerCSS"):
        get_beercss_dir(tmp_path)
