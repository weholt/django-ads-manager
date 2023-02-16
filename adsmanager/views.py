from django.shortcuts import redirect

from adsmanager.services import get_ad, log_click


def ad_redirect(request, ad_uuid):
    ad = get_ad(ad_uuid)
    log_click(request, ad)

    response = redirect(ad.target_link)
    response.set_cookie("ads-manager-sleep", "1", max_age=ad.sleep_time_minutes * 60)
    return response
