from .base import *


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ":memory",
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
