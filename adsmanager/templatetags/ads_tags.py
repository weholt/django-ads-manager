from django import template
from django.urls import reverse

from adsmanager.services import get_random_ad

register = template.Library()


@register.inclusion_tag("ads/ad.html", takes_context=True)
def get_random_add(context):
    request = context.get("request")
    ad = get_random_ad(request)
    if ad:
        return {"ad": ad, "link": reverse("adsmanager:ad-redirect", args=[ad.uuid])}
