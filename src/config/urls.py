from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls

from apps.core.views import favicon
from apps.search import views as search_views

urlpatterns = [
    path("favicon.ico", favicon),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("intentional-blanks/", include("wagtail_localize_intentional_blanks.urls")),
]

urlpatterns += i18n_patterns(
    path("search/", search_views.search, name="search"),
    # For anything not caught by a more specific rule above,
    # hand over to Wagtail's page serving mechanism.
    # This should be the last pattern in the list:
    path("", include(wagtail_urls)),
)


if "debug_toolbar" in settings.INSTALLED_APPS:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
