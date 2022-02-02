from django.conf import settings
import os

RAVEPAY_SECRET_KEY = 'FLWSECK_TEST-aa528235ea8465216753394deccb2beb-X'
RAVEPAY_PUBLIC_KEY = 'FLWPUBK_TEST-f56a181128b8edde1c201c84114c75a5-X'

# RAVEPAY_SECRET_KEY = 'FLWSECK-f5cefec0505eb5a8a14970aa37d49a2a-X'
# RAVEPAY_PUBLIC_KEY = 'FLWPUBK-bcf023d60ead2cc5901fff8dddef812d-X'
ALLOWED_HOSTS = getattr(settings, "ALLOWED_HOSTS", [])
RAVEPAY_WEBHOOK_DOMAIN = getattr(settings, "RAVEPAY_WEBHOOK_DOMAIN", None)
if RAVEPAY_WEBHOOK_DOMAIN:
    ALLOWED_HOSTS.append(RAVEPAY_WEBHOOK_DOMAIN)
RAVEPAY_FAILED_URL = getattr(settings, "RAVEPAY_FAILED_URL", "ravepay:failed_page")
RAVEPAY_SUCCESS_URL = getattr(settings, "RAVEPAY_SUCCESS_URL", "ravepay:success_page")
TEST_RAVEPAY_API_URL = "https://ravesandboxapi.flutterwave.com/flwv3-pug/getpaidx"
RAVEPAY_API_URL = "https://api.ravepay.co/flwv3-pug/getpaidx"
RAVEPAY_MODAL_TITLE = getattr(
    settings, "RAVEPAY_MODAL_TITLE", os.getenv("RAVEPAY_MODAL_TITLE", "Test Account")
)
RAVEPAY_MODAL_LOGO = getattr(
    settings, "RAVEPAY_MODAL_LOGO", os.getenv("RAVEPAY_MODAL_LOGO", "")
)
RAVEPAY_LIB_MODULE = getattr(settings, "RAVEPAY_LIB_MODULE", "ravepay.utils")
RAVEPAY_WEBHOOK_HASH = getattr(settings, "RAVEPAY_WEBHOOK_HASH", "DJANGO_RAVEPAY")

