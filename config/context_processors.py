from hashlib import md5

from django.conf import settings
from django_ftl.templatetags.ftl import BUNDLE_VAR_NAME, MODE_VAR_NAME

from wagtail.models import Page

from apps.core.ftl_bundles import main

EXPORTED_SETTINGS = ["ENVIRONMENT", "GOATCOUNTER_URL"]


def app(request):
    slugs = "".join(Page.objects.live().only("slug").values_list("slug", flat=True))
    lang = request.LANGUAGE_CODE
    hexdigest = md5(slugs.encode()).hexdigest()
    return {
        "CACHE_BURST": f"{lang}-{hexdigest}",
        "TIMEOUT": settings.CACHE_TIMEOUT_SEC,
        **{s: getattr(settings, s, None) for s in EXPORTED_SETTINGS},
    }


def fluent(request):
    return {BUNDLE_VAR_NAME: main, MODE_VAR_NAME: "server"}
