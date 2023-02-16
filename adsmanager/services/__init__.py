import random
from datetime import date, datetime, timedelta
from typing import Iterable, Union

from django.db.models import Q
from django.http import HttpRequest

from adsmanager.models import Ad, AdClick


def get_active_ads() -> Iterable[Ad]:
    today = date.today()
    return Ad.objects.filter((Q(active_from_time__isnull=True) | Q(active_from_time__lt=today)) & Q(active_to_time__isnull=True) | Q(active_to_time__gt=today))


def randomize_ads() -> Union[None, Ad]:
    ads = []
    for a in get_active_ads():
        for i in range(0, a.weight):
            ads.append(a)

    if ads:
        return random.choice(ads)


def get_random_ad(request: HttpRequest) -> Union[Ad, None]:
    "Get a random ad, if the user has not seen an ad already"
    has_seen_ad = request.COOKIES.get("ads-manager-sleep", "")
    if has_seen_ad:
        return

    ad = randomize_ads()

    if ad:
        ad.display_count += 1
        ad.save(update_fields=["display_count"])
        return ad


def get_ad(ad_uuid) -> Ad:
    "Get a specific ad by uuid"
    return Ad.objects.get(uuid=ad_uuid)


def log_click(request, ad: Ad) -> None:
    "Logs if a user has clicked on an ad, but only every 5 minutes"
    dt = datetime.now() - timedelta(minutes=5)
    if not AdClick.objects.filter(ad=ad, user=request.user, created__lt=dt).exists():
        ad.click_count += 1
        ad.save(update_fields=["click_count"])

        ip = request.META.get("REMOTE_ADDR", None)
        accept_language = request.META.get("HTTP_ACCEPT_LANGUAGE", None)
        referer = request.META.get("HTTP_REFERER", None)
        user_agent = request.META.get("HTTP_USER_AGENT", None)
        AdClick.objects.create(user=request.user, ad=ad, ip=ip, referer=referer, user_agent=user_agent, accept_language=accept_language)
