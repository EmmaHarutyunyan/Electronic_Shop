from django.conf import settings 

from appconf import AppConf

__all__ = ["settings"]


class CookieConsentConf(AppConf):
    NAME = "cookie_consent"
    # TODO: 
    MAX_AGE = 60 * 60 * 24 * 365 * 1 
    DOMAIN = None
    SECURE = False
    HTTPONLY = True
    SAMESITE = "Lax"

    DECLINE = "-1"

    ENABLED = True

    OPT_OUT = False

    CACHE_BACKEND = "default"

    LOG_ENABLED = True