# flake8: noqa
from .settings_shared import *
import sys


TEMPLATE_DIRS = (
    "/var/www/smilekit/smilekit/smilekit/templates",
)

MEDIA_ROOT = '/var/www/capsim/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/capsim/capsim/sitemedia'),
)

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django')
    import logging
    from raven.contrib.django.handlers import SentryHandler
    logger = logging.getLogger()
    # ensure we havent already registered the handler
    if SentryHandler not in map(type, logger.handlers):
        logger.addHandler(SentryHandler())
        logger = logging.getLogger('sentry.errors')
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())

    SENTRY_KEY = 'EWv5EELZnZIrOY'
    SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

try:
    from local_settings import *
except ImportError:
    pass
