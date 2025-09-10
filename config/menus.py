from dataclasses import asdict, dataclass

from apps.core.ftl_bundles import main

t = main.format_lazy


@dataclass
class MenuItem:
    title: str
    icon: str
    subitems: "list[MenuItem] | None" = None


@dataclass
class Menu:
    items: list[MenuItem]


module_menu = [
    MenuItem(
        title=t("app-modules-about-language"),
        icon="emoji_language",
    ),
    MenuItem(
        title=t("app-modules-about-history"),
        icon="dictionary",
    ),
    MenuItem(
        title=t("app-modules-about-eu"),
        icon="flag",
    ),
]

main_menu = asdict(
    Menu(
        items=[
            # MenuItem(title=t("app-about-the-project"), icon="question_mark"),
            MenuItem(title=t("app-comics"), icon="comic_bubble"),
            MenuItem(
                title=t("app-modules"),
                icon="apps",
                subitems=module_menu,
            ),
            MenuItem(title=t("app-methodology"), icon="tactic"),
        ]
    )
)["items"]
