from typing import TYPE_CHECKING

from django.conf import settings
from wagtail import hooks

if TYPE_CHECKING:
    from wagtail.models import Page
    from wagtailmenus.models import FlatMenuItem


@hooks.register("construct_page_action_menu")
def reorder_page_actions(menu_items, request, context):
    if not settings.DEBUG:
        return

    items = {item.name: item for item in menu_items}
    items["action-publish"].order = 0  # Default button
    items["action-save-draft"].order = 80  # Higher than 60, less than default 100
    menu_items[:] = sorted(items.values(), key=lambda i: i.order)


def localized_page_or_menu_item(item: FlatMenuItem) -> FlatMenuItem | Page:
    return item.link_page.localized if item.link_page else item


@hooks.register("menus_modify_raw_menu_items")
def localize_menu_items(menu_items, menu_tag, **kwargs):
    if menu_tag == "flat_menu":
        return map(localized_page_or_menu_item, menu_items)
    return menu_items
