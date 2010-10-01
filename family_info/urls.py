from django.conf.urls.defaults import *
from django.conf import settings
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
  (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
  (r'^families$',                             'family_info.views.families'),
  (r'^new_family$',                           'family_info.views.new_family'),
  (r'^insert_family$',                        'family_info.views.insert_family'),
  (r'^edit_family/(?P<family_id>\d+)$',       'family_info.views.edit_family'),
  
  (r'^new_user$',                             'family_info.views.new_user'),
  (r'^insert_user$',                          'family_info.views.insert_user'),
  (r'^edit_user/(?P<user_id>\d+)$',           'family_info.views.edit_user'),
  
  
  (r'^start_interview/(?P<family_id>\d+)$',   'family_info.views.start_interview'),
  (r'^wrap_up_interview$',                    'family_info.views.wrap_up_interivew'),
  (r'^end_interview$',                        'family_info.views.end_interview'),
  
)
