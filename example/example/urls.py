from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


class TestView(TemplateView):
    template_name = "app1/index.html"


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TestView.as_view()),
    path("", include("adsmanager.urls"))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
