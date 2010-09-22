from django.conf.urls.defaults import *
from django.conf import settings
import os.path


urlpatterns = patterns('',
  (r'login$',                    'family_info.views.login'), 
  (r'participants$',             'family_info.views.participants'), 
  (r'family_assessment$',        'family_info.views.family_assessment'),
  (r'family_information$',       'family_info.views.family_information'), 
  (r'health_worker_information$','family_info.views.health_worker_information'), 
  (r'sync$',                     'family_info.views.sync')  
)


if 1 == 0:
  instructions = """
        	

      where researchers can:
      1. add health worker user accounts
      2. add families
      3. lock families for local storage
      4. go to client facing tool

      note - some activities can only be done on computer/some on mobile device


	
"""



