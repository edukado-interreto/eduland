from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path

from apps.core.views import home_page

urlpatterns = [
    path("admin/", admin.site.urls),
]
urlpatterns += i18n_patterns(
    path("", home_page),
)
