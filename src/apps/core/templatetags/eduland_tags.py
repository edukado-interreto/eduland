from django import template
from django.template.loader import render_to_string

from config import menus

register = template.Library()


@register.simple_tag
def icon(name: str, css_class: str = "") -> str:
    """Inline SVG icon from apps/theme/templates/icons/, e.g. {% icon "menu" "size-8" %}"""
    return render_to_string(f"icons/{name}.svg", {"class": css_class})


@register.inclusion_tag("core/preload_css.html")
def preload_css(url: str):
    """Load a stylesheet without blocking the rendering"""
    return {"url": url}


@register.simple_tag(takes_context=True)
def main_menu(context):
    return menus.main_menu()
