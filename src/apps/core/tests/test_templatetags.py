from django.template import Context, Template

from apps.core.templatetags.eduland_tags import icon
from config.menus import MenuItem, get_menu_items


def test_icon_inlines_svg():
    svg = icon("menu", "size-8")
    assert svg.startswith("<svg ")
    assert 'class="icon size-8"' in svg
    assert 'aria-hidden="true"' in svg


def test_icon_without_extra_class():
    assert 'class="icon"' in icon("translate")


def test_icon_tag_with_variable():
    template = Template('{% load eduland_tags %}{% icon name "size-6" %}')
    assert "<svg " in template.render(Context({"name": "chevron_right"}))


def test_every_menu_icon_exists(monkeypatch):
    """The menu icons are names of the SVG files of apps/theme/templates/icons/."""
    monkeypatch.setattr("config.menus.page", lambda slug: None)
    monkeypatch.setattr("config.menus.shown", lambda *items: list(items))

    def walk(items: list[MenuItem]):
        for item in items:
            yield item.icon
            yield from walk(item.subitems or [])

    for name in walk(get_menu_items()):
        assert "<svg " in icon(name), name
