# Django settings for smilekit project.
import os.path
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'smilekit',
        'HOST': '',
        'PORT': '',
        'USER': '',
        'PASSWORD': '',
    }
}

CACHE_BACKEND = 'locmem://'

if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }

SOUTH_TESTS_MIGRATE = False
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    ('--cover-package=smilekit.equation_balancer,smilekit.collection_tool'
     ',smilekit.family_info'),
]
JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pep8',
)
PROJECT_APPS = [
    'smilekit.family_info', 'smilekit.equation_balancer',
    'smilekit.collection_tool',
]


TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/smilekit/uploads/"
MEDIA_URL = '/uploads/'
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'djangowind.context.context_processor',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'waffle.middleware.WaffleMiddleware',
)

ROOT_URLCONF = 'smilekit.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

STATIC_URL = "/media/"
STATICFILES_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../media/")),
)
STATIC_ROOT = ""
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'sorl.thumbnail',
    'django.contrib.admin',
    'tagging',
    'smartif',
    'template_utils',
    'typogrify',
    'tinymce',
    'smilekit.family_info',
    'smilekit.collection_tool',
    'smilekit.equation_balancer',
    'django_nose',
    'django_jenkins',
    'south',
    'smoketest',
    'waffle',
    'django_statsd',
    'django_markwhat',
    'django.contrib.staticfiles',
]

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[smilekit] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "smilekit@ccnmtl.columbia.edu"

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'smilekit'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125
#STATSD_PATCHES = ['django_statsd.patches.db', ]

# WIND settings

AUTHENTICATION_BACKENDS = ('djangowind.auth.SAMLAuthBackend',
                           'django.contrib.auth.backends.ModelBackend',)
CAS_BASE = "https://cas.columbia.edu/"
WIND_PROFILE_HANDLERS = ['djangowind.auth.CDAPProfileHandler']
WIND_AFFIL_HANDLERS = ['djangowind.auth.AffilGroupMapper',
                       'djangowind.auth.StaffMapper',
                       'djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlc.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = ['anp8', 'jb2410', 'zm4', 'sbd12', 'egr2107',
                                'sld2131', 'amm8', 'mar227', 'ed2198']

TINYMCE_JS_URL = '/media/js/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = 'media/js/tiny_mce'

TINYMCE_COMPRESSOR = False
TINYMCE_SPELLCHECKER = True

TINYMCE_DEFAULT_CONFIG = {'cols': 80,
                          'rows': 30,
                          'plugins': 'table,spellchecker,paste,searchreplace',
                          'theme': 'simple',
                          }

ALLOWED_HOSTS = ['.ccnmtl.columbia.edu', 'localhost']
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
LOGIN_REDIRECT_URL = "/"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
