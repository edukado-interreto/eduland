from http import HTTPStatus

from wagtail.models import Locale

import pytest


@pytest.fixture
def translated_home(home_page):
    """French translation of the home page, in its own locale tree."""
    french = Locale.objects.get_or_create(language_code="fr")[0]
    translation = home_page.copy_for_translation(french)
    translation.save_revision().publish()
    return translation


def test_sitemap_lists_translations_with_alternates(client, home_page, translated_home):
    response = client.get("/sitemap.xml")
    assert response.status_code == HTTPStatus.OK
    content = response.content.decode()

    for page in (home_page, translated_home):
        url = page.get_full_url()
        assert f"<loc>{url}</loc>" in content
        hreflang = page.locale.language_code
        assert f'hreflang="{hreflang}" href="{url}"' in content
