from http import HTTPStatus

from wagtail.models import Page

import pytest

from apps.education.models import (
    ExercisePage,
    MethodologyPage,
    ModulePage,
    UnitPage,
)
from apps.home.models import HomePage, NewsIndexPage, NewsPost, SimplePage


@pytest.mark.parametrize(
    ("model", "parents"),
    [
        (HomePage, {Page}),
        (ModulePage, {HomePage}),
        (MethodologyPage, {HomePage}),
        (UnitPage, {ModulePage, MethodologyPage}),
        (ExercisePage, {UnitPage}),
        (SimplePage, {HomePage}),
        (NewsIndexPage, {HomePage}),
        (NewsPost, {NewsIndexPage}),
    ],
)
def test_page_tree(model, parents):
    assert set(model.allowed_parent_page_models()) == parents


def test_exercise_page_is_a_leaf():
    assert ExercisePage.allowed_subpage_models() == []


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name",
    ["home", "module", "methodology", "unit", "exercise", "news", "post", "simple"],
)
def test_page_renders(client, page_tree, name):
    page = page_tree[name]
    response = client.get(page.url)
    assert response.status_code == HTTPStatus.OK
    assert page.title in response.text


@pytest.mark.django_db
def test_exercise_page_includes_the_data(client, page_tree, exercise):
    response = client.get(page_tree["exercise"].url)
    assert 'id="exercise-data"' in response.text
    assert "Ahoj" in response.text


@pytest.mark.django_db
def test_home_page_lists_live_children(page_tree):
    home = page_tree["home"]
    hidden = home.add_child(instance=ModulePage(title="Draft module", live=False))

    assert list(home.module_pages()) == [page_tree["module"].page_ptr]
    assert hidden.page_ptr not in home.module_pages()
    assert list(home.methodology_pages()) == [page_tree["methodology"].page_ptr]


@pytest.mark.django_db
def test_unit_page_lists_live_exercises(page_tree):
    unit = page_tree["unit"]
    unit.add_child(instance=ExercisePage(title="Draft exercise", live=False))
    assert list(unit.exercise_pages()) == [page_tree["exercise"].page_ptr]


@pytest.mark.django_db
def test_search(client, page_tree):
    response = client.get("/en/search/", {"query": "Launch"})
    assert response.status_code == HTTPStatus.OK
    assert page_tree["post"].url in response.text


@pytest.mark.django_db
def test_root_redirects_to_language(client, home_page):
    response = client.get("/")
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/en/"
