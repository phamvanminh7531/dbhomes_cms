from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ua7=zkvy9-8z+b6ssqt#bq9f)npzxy4&*&9^3=a7_@7pv#8lj2"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # ✅
EMAIL_HOST_USER = 'phamvanminh7531@gmail.com'
EMAIL_HOST_PASSWORD = 'suqd yicq hjwx eqdb'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

ADMINS = [('Admin', 'dbplusai@gmail.com')]


# Admin nhận thông báo
ADMINS = [('Admin', 'dbplusai@gmail.com')]

try:
    from .local import *
except ImportError:
    pass
