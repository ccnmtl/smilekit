import os, sys, site

# paths we might need to pick up the project's settings
sys.path.append('/var/www/smilekit/smilekit/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'smilekit.settings_staging'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
