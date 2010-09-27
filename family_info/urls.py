from django.conf.urls.defaults import *
from django.conf import settings
import os.path


urlpatterns = patterns('',
  #(r'login$',                    'family_info.views.login'), 
  #(r'participants$',             'family_info.views.participants'), 
  #(r'family_assessment$',        'family_info.views.family_assessment'),
  #(r'family_information$',       'family_info.views.family_information'), 
  #(r'health_worker_information$','family_info.views.health_worker_information'), 
  
  
  (r'^families$',                             'family_info.views.families'),
  (r'^sync$',                                 'family_info.views.sync'),
  (r'^new_family$',                           'family_info.views.new_family'),
  (r'^insert_family$',                        'family_info.views.insert_family'),
  (r'^edit_family/(?P<family_id>\d+)$',       'family_info.views.edit_family'),
  (r'^new_user$',                             'family_info.views.new_user'),
  (r'^insert_user$',                          'family_info.views.insert_user'),
  (r'^edit_user/(?P<user_id>\d+)$',           'family_info.views.edit_user'),
)
