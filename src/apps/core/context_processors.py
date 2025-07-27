from django_ftl.templatetags.ftl import BUNDLE_VAR_NAME, MODE_VAR_NAME

from apps.core.ftl_bundles import main


def fluent(request):
    return {BUNDLE_VAR_NAME: main, MODE_VAR_NAME: "server"}
