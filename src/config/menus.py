from dataclasses import asdict, dataclass

from django.utils.translation import activate, get_language

from wagtail.models import Locale, Page

from apps.core.ftl_bundles import main

ENGLISH = Locale.objects.get(language_code="en")

t = main.format_lazy


@dataclass
class MenuItem:
    icon: str
    page: Page | None = None
    title: str | None = None
    subitems: "list[MenuItem] | None" = None


@dataclass
class Menu:
    items: list[MenuItem]


def page(slug) -> Page:
    try:
        return Page.objects.get(slug=slug, locale=ENGLISH).localized
    except Page.DoesNotExist:
        return Page.objects.filter(locale=ENGLISH).first()


menu_items = [
    MenuItem(
        icon="apps",
        title=t("app-modules"),
        subitems=[
            MenuItem("emoji_language", page=page("crash-course")),
            MenuItem("dictionary", page=page("about-history")),
            MenuItem("flag", page=page("about-eu")),
        ],
    ),
    MenuItem(
        icon="newsmode",
        title=t("app-news"),
        page=page("news"),
    ),
    MenuItem(
        icon="info",
        title=t("app-about-the-project"),
        page=page("about"),
    ),
]


main_menu = asdict(Menu(menu_items))["items"]
