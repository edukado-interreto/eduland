from dataclasses import asdict, dataclass

from wagtail.models import Locale, Page

from apps.core.ftl_bundles import main

ENGLISH = Locale.objects.get(language_code="en")

t = main.format_lazy


@dataclass
class MenuItem:
    icon: str
    page: Page | None = None
    title: str | None = None
    subitems: list[MenuItem] | None = None


@dataclass
class Menu:
    items: list[MenuItem]


def page(slug) -> Page | None:
    english_page = Page.objects.filter(slug__icontains=slug, locale=ENGLISH).first()
    return english_page.localized if english_page else None


def is_shown(item: MenuItem) -> bool:
    if item.subitems is not None:
        return bool(item.subitems)
    return item.page is not None and item.page.live and item.page.show_in_menus


def shown(*items: MenuItem) -> list[MenuItem]:
    return [item for item in items if is_shown(item)]


def get_menu_items() -> list[MenuItem]:
    return shown(
        MenuItem(
            icon="apps",
            title=t("app-modules"),
            subitems=shown(
                MenuItem("emoji_language", page=page("crash-course")),
                MenuItem("military_tech", page=page("about-history")),
                MenuItem("flag", page=page("about-eu")),
            ),
        ),
        MenuItem(
            icon="cognition_2",
            title=t("app-methodology"),
            subitems=shown(
                MenuItem("auto_stories", page=page("guided-reading")),
                MenuItem("globe_book", page=page("content-and-language")),
            ),
        ),
        MenuItem(
            icon="newsmode",
            title=t("app-news"),
            page=page("news"),
        ),
        MenuItem(
            icon="info",
            title=t("app-about-the-project"),
            subitems=shown(
                MenuItem(icon="info", page=page("about-eduland")),
                MenuItem(icon="mail", page=page("contact-us")),
            ),
        ),
    )


def main_menu():
    return asdict(Menu(get_menu_items()))
