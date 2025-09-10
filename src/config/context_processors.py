from django.conf import settings
from django_ftl.templatetags.ftl import BUNDLE_VAR_NAME, MODE_VAR_NAME

from apps.core.ftl_bundles import main
from config.menus import main_menu

EXPORTED_SETTINGS = []


def app(request):
    menus = {"main_menu": main_menu}
    exported_settings = {s: getattr(settings, s) for s in EXPORTED_SETTINGS}
    return {**menus, **exported_settings}


def fluent(request):
    return {BUNDLE_VAR_NAME: main, MODE_VAR_NAME: "server"}
