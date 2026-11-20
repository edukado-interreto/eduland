from hashlib import md5

from django.conf import settings
from django_ftl.templatetags.ftl import BUNDLE_VAR_NAME, MODE_VAR_NAME

from wagtail.models import Page

from apps.core.ftl_bundles import main

EXPORTED_SETTINGS = ["ENVIRONMENT", "GOATCOUNTER_URL"]


def _cache_burst(request):
    lang = request.LANGUAGE_CODE
    live_pages = Page.objects.live().order_by("pk").values_list("slug", "show_in_menus")
    fingerprint = "".join(f"{slug}:{int(in_menus)};" for slug, in_menus in live_pages)
    hexdigest = md5(fingerprint.encode()).hexdigest()

    return f"{lang}-{hexdigest}"


def app(request):
    return {
        "CACHE_BURST": _cache_burst(request),
        "TIMEOUT": settings.CACHE_TIMEOUT_SEC,
        **{s: getattr(settings, s, None) for s in EXPORTED_SETTINGS},
    }


def fluent(request):
    return {BUNDLE_VAR_NAME: main, MODE_VAR_NAME: "server"}
