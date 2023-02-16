import os
from uuid import uuid4

from django.contrib.auth import get_user_model

# from django.core.cache import cache
from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        # set filename as random string
        filename = "{}.{}".format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


image_handler = PathAndRename("ads")

User = get_user_model()


class Ad(models.Model):
    """
    Ad
    """

    uuid = models.UUIDField(default=uuid4, editable=False)
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ads")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    image = models.ImageField(upload_to=image_handler)
    target_link = models.URLField()
    link_text = models.CharField(max_length=100)
    weight = models.PositiveIntegerField(default=1)
    sleep_time_minutes = models.PositiveIntegerField(default=5)
    open_new_window = models.BooleanField(default=True)
    active_from_time = models.DateTimeField(null=True, blank=True)
    active_to_time = models.DateTimeField(null=True, blank=True)
    display_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)
    show_link_text = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class AdClick(models.Model):
    "Logs each time a user clicks the ad"
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="user_clicks")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="clicked_ads")
    created = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    accept_language = models.CharField(max_length=50, null=True, blank=True)
    referer = models.CharField(max_length=150, null=True, blank=True)
    user_agent = models.CharField(max_length=250, null=True, blank=True)
