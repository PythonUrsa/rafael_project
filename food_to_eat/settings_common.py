
ADMINS = (
    ('soporte', 'soporte@trea.uy'),
)
MANAGERS = ADMINS

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(__file__)
ROOT_URLCONF = 'food_to_eat.urls'

SECRET_KEY = 'vi7jp5_tvx=a_q%$t=$xvqp+b3=k#_up84__t(&24jd2_kqcj8'


INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'custom_user',
    'fte_users',
    'fte_restaurants',
    'fte_admin',
    'location_field',
    'daterange_filter',
    'tastypie',
    'djangobower',
    'sorl.thumbnail',
    'corsheaders',
    'simple_email_confirmation',
    'django_summernote',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True

SESSION_COOKIE_HTTPONLY = True

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

MEDIA_URL = '/media/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),

)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.tz",
                               "django.contrib.messages.context_processors.messages",
                               "django.core.context_processors.request",
                               )

# Permito que un usuario se registre con su email en lugar de un username.
AUTH_USER_MODEL = 'fte_users.FTEUser'

GRAPPELLI_ADMIN_TITLE = "Food to Eat - Administration"


BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'fte_restaurants/components')

BOWER_INSTALLED_APPS = (
    'angular',
    'jquery',
    'jquery-ui',
    'angular-bootstrap',
    'angular-ui-router',
    'underscore',
    'angular-resource',
    'angucomplete-alt',
    'angular-spinner',
    'angular-google-maps',
    'underscore.string',
    'angular-cookies',
    'angularjs-imageupload-directive',
    'angular-sanitize',
    'angular-social-links',
)




