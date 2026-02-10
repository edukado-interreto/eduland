from django import template
from wagtail.models import Site

from config import menus

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page.localized


@register.simple_tag(takes_context=True)
def for_current_locale(context, page):
    locale = context["page"].locale
    return page.get_translation(locale)


@register.simple_tag(takes_context=True)
def main_menu(context):
    return menus.main_menu()
