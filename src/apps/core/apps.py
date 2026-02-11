from django.apps import AppConfig
from wagtail.images.apps import WagtailImagesAppConfig


class CoreConfig(AppConfig):
    name = "apps.core"


class CustomImagesAppConfig(WagtailImagesAppConfig):
    default_attrs = {"decoding": "async", "loading": "lazy"}
