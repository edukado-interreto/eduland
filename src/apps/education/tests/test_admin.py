import json
from http import HTTPStatus

from django.urls import reverse

import pytest

from apps.education.models import Exercise

pytestmark = pytest.mark.django_db

FORM = {
    "name": "M1 U1 02",
    "title": "Numbers",
    "src_lang": "fr",
    "lang_learn_lang": "sk",
    "lang_learn_cefr_level_min": Exercise.CEFR.A1,
    "lang_learn_cefr_level_max": Exercise.CEFR.B1,
    "age_min": 10,
    "age_max": 18,
}


def test_create_exercise_opens_the_editor(admin_client, admin_user):
    response = admin_client.post(
        reverse("wagtailsnippets_education_exercise:add"), FORM
    )

    exercise = Exercise.objects.get(name="M1 U1 02")
    assert exercise.created_by == admin_user
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse("exercise_editor", kwargs={"pk": exercise.pk})


def test_exercise_list(admin_client, exercise):
    response = admin_client.get(reverse("wagtailsnippets_education_exercise:list"))
    assert response.status_code == HTTPStatus.OK
    assert exercise.name in response.text


def test_editor_collapses_the_sidebar(admin_client, exercise):
    response = admin_client.get(reverse("exercise_editor", kwargs={"pk": exercise.pk}))
    assert response.status_code == HTTPStatus.OK
    assert response.cookies["wagtail_sidebar_collapsed"].value == "1"


def test_editor_saves_the_data(admin_client, exercise):
    data = {"sheet": [{"type": "text", "content": "Dobrý deň"}]}
    response = admin_client.post(
        reverse("exercise_editor", kwargs={"pk": exercise.pk}),
        {"data": json.dumps(data)},
    )

    exercise.refresh_from_db()
    assert exercise.data == data
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == exercise.get_absolute_url()
    assert response.cookies["wagtail_sidebar_collapsed"].value == "0"


def test_editor_requires_login(client, exercise):
    response = client.get(reverse("exercise_editor", kwargs={"pk": exercise.pk}))
    assert response.status_code == HTTPStatus.FOUND
    assert "/admin/login/" in response.url
