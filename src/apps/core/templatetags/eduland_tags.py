from django import template
from django.conf import settings
from django.templatetags.static import StaticNode

from config import menus, utils

register = template.Library()


BEERCSS_DIR = utils.get_beercss_dir(static_dir=settings.STATICFILES_DIRS[0])


class BeerCssNode(StaticNode):
    def url(self, context):
        filename = self.path.resolve(context)
        path = f"{BEERCSS_DIR}/{filename}"
        return self.handle_simple(path)


@register.tag("beercss")
def do_beercss(parser, tokens):
    """Handle BeerCSS version just as the {% static %} tag."""
    return BeerCssNode.handle_token(parser, tokens)


@register.simple_tag(takes_context=True)
def main_menu(context):
    return menus.main_menu()
