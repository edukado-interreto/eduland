from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path

from apps.core.views import home_page, favicon

urlpatterns = [
    path("favicon.ico", favicon),
    path("admin/", admin.site.urls),
]
urlpatterns += i18n_patterns(
    path("", home_page, name="home"),
)
