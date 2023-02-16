from django.urls import path

from .views import ad_redirect

app_name = "adsmanager"

urlpatterns = [path("adrir/<uuid:ad_uuid>", ad_redirect, name="ad-redirect")]
