from food_to_eat.settings_common import *

ALLOWED_HOSTS = ['*']

#Production DataBase Settings

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'food_to_eat',                      # Or path to database file if using sqlite3.
        'USER': 'food_to_eat',                      # Not used with sqlite3.
        'PASSWORD': 'f2ef2ef2eF2EF2E',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

DEBUG = False

TEMPLATE_DEBUG = False

WSGI_APPLICATION = 'food_to_eat.wsgi_production.application'

'''
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = "email-smtp.us-east-1.amazonaws.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = 'AKIAJVILWMIXQWL3TMRA'
EMAIL_HOST_PASSWORD = 'Anxd0ImMYPYVW1bWYipubTOr81rMtCwB3Ec5P35ZsrL7'
EMAIL_USE_TLS = True
'''

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'testing@example.com'
 
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER


STATIC_ROOT = '/home/food_to_eat/static'

MEDIA_ROOT = '/home/food_to_eat/media/'
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
MEDIA_URL = '/media/'

EMAIL_CONFIRMATION_URL = "http://www.deliveryrd.do/user/api/confirm_email/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(module)s %(process)d %(thread)d - %(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(name)s - %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter' : 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/logs/production_log.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console','file'],
            'level' : 'DEBUG',
            'propagate' : True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'fte_admin.resources': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'fte_restaurant': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'fte_users': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
