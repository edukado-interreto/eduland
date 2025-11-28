from django.conf import settings
from wagtail import hooks


@hooks.register("construct_page_action_menu")
def reorder_page_actions(menu_items, request, context):
    if not settings.DEBUG:
        return

    items = {item.name: item for item in menu_items}
    items["action-publish"].order = 0  # Default button
    items["action-save-draft"].order = 80  # Higher than 60, less than default 100
    menu_items[:] = sorted(items.values(), key=lambda i: i.order)
