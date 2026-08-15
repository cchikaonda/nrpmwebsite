from .base import *

DEBUG = False

SECRET_KEY = "django-insecure-k9qj_mq84)i*zj&^41gdg649rdm)u_*jq7dlzjn=mjl6n%fszl"

ALLOWED_HOSTS = [
    "newresmi.org",
    "www.newresmi.org",
    "147.93.121.208",
    "localhost",
    "127.0.0.1",
]

STATIC_URL = "/static/"
STATIC_ROOT = "/var/www/nrpmwebsite/staticfiles/"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/var/www/nrpmwebsite/media/"


CSRF_TRUSTED_ORIGINS = [
    "http://newresmi.org",
    "http://www.newresmi.org",
]

WAGTAILADMIN_BASE_URL = "http://newresmi.org"

STORAGES["staticfiles"]["BACKEND"] = (
    "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
)

try:
    from .local import *
except ImportError:
    pass
