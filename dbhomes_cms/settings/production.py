from dotenv import load_dotenv
from .base import *

# Load environment variables from .env file
load_dotenv()


# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # ✅
EMAIL_HOST_USER = "phamvanminh7531@gmail.com"
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

ADMINS = [("Admin", "dbplusai@gmail.com")]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql", 
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USER'),
        "PASSWORD": os.getenv('DB_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
    }
}

try:
    from .local import *
except ImportError:
    pass
