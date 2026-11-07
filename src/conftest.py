from django.core.cache import cache

from wagtail.models import Page, Site

import pytest

from apps.education.models import (
    Exercise,
    ExercisePage,
    MethodologyPage,
    ModulePage,
    UnitPage,
)
from apps.home.models import HomePage, NewsIndexPage, NewsPost, SimplePage


@pytest.fixture(autouse=True)
def clear_cache():
    """Views and templates are cached (cache_page, wagtailpagecache)."""
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def home_page(db):
    """Home page as root of the default site, next to Wagtail’s welcome page."""
    home = Page.get_first_root_node().add_child(
        instance=HomePage(
            title="EduLand",
            slug="eduland",
            hero_cta=[("button", {"text": "Start", "url": "#modules"})],
        )
    )
    Site.objects.update(root_page=home)
    return home


@pytest.fixture
def exercise(db):
    return Exercise.objects.create(
        name="M1 U1 01",
        title="Greetings",
        src_lang="fr",
        lang_learn_lang="sk",
        data={"sheet": [{"type": "text", "content": "Ahoj"}]},
    )


@pytest.fixture
def page_tree(home_page, exercise):
    """One page of each type, as they are organised on the website."""
    module = home_page.add_child(instance=ModulePage(title="Crash course"))
    methodology = home_page.add_child(instance=MethodologyPage(title="Methodology"))
    unit = module.add_child(instance=UnitPage(title="Unit 1"))
    exercise_page = unit.add_child(
        instance=ExercisePage(title="Exercise 1", exercise=exercise)
    )
    news = home_page.add_child(instance=NewsIndexPage(title="News"))
    post = news.add_child(instance=NewsPost(title="Launch", standfirst="It starts"))
    simple = home_page.add_child(instance=SimplePage(title="About EduLand"))
    return {
        "home": home_page,
        "module": module,
        "methodology": methodology,
        "unit": unit,
        "exercise": exercise_page,
        "news": news,
        "post": post,
        "simple": simple,
    }
