import pytest

from apps.education.models import Exercise, display_language


def test_display_language():
    assert display_language("eo") == "Esperanto"
    assert display_language("xx") == "N/A"


def test_str():
    exercise = Exercise(name="M1 U1 01", title="Greetings", lang_learn_lang="sk")
    assert str(exercise) == "M1 U1 01 • Slovak • Greetings"


def test_str_without_title():
    exercise = Exercise(name="M1 U1 01", lang_learn_lang="sk")
    assert str(exercise) == "M1 U1 01 • Slovak"


def test_languages():
    exercise = Exercise(src_lang="fr", lang_learn_lang="eo")
    assert exercise.language == "French"
    assert exercise.teaching == "Esperanto"


@pytest.mark.parametrize(
    ("data", "empty"),
    [
        ({"sheet": [{"type": "text"}]}, False),
        ({"sheet": []}, True),
        ({}, True),
        ([], True),
        (None, True),
    ],
)
def test_has_empty_data(data, empty):
    assert Exercise(data=data).has_empty_data is empty


def test_new_exercise_has_empty_data():
    assert Exercise().has_empty_data


@pytest.mark.django_db
def test_lid_is_unique(exercise, monkeypatch):
    monkeypatch.setattr("apps.education.models.long_id", lambda: "newlid1")
    duplicate = Exercise.objects.create(name="Copy", lid=exercise.lid)
    assert duplicate.lid == "newlid1"


@pytest.mark.django_db
def test_lid_kept_on_update(exercise):
    lid = exercise.lid
    exercise.title = "Hello"
    exercise.save()
    exercise.refresh_from_db()
    assert exercise.lid == lid
