# django-ads-manager

A reusable django app for managing simple ads.

## Installation

```
pip install -e git+git://github.com/weholt/django-ads-manager.git#egg=adsmanager
```

Add 'sveve' to your INSTALLED_APPS before 'django.contrib.admin':
```
INSTALLED_APPS = [
    "django.contrib.admin",
    ...
    "django.contrib.staticfiles",
    "adsmanager",
]
```

Add the sveve urls to your global urls.py:
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    ...
    path("", include("adsmanager.urls"))
]
```

Now in your templates you load the required templatetags:

```
{% load ads_tags %}
```

And to display an ad, place this somewhere in your template:
```
{% get_random_add %}
```

Over in the admin, you can load an image (your ad), and configure how often you want it to show. The default is in 5 minutes intervals.

## Version history

0.1.0 :
 - Initial MVP - release.