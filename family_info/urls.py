from django.conf.urls.defaults import *
from django.conf import settings
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
  (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
  (r'^families/$',                             'family_info.views.families'),
  (r'^new_family/$',                           'family_info.views.new_family'),
  (r'^insert_family/$',                        'family_info.views.insert_family'),
  (r'^edit_family/(?P<family_id>\d+)/$',       'family_info.views.edit_family'),
  (r'^new_user/$',                             'family_info.views.new_user'),
  (r'^insert_user/$',                          'family_info.views.insert_user'),
  (r'^edit_user/(?P<user_id>\d+)/$',           'family_info.views.edit_user'),
  (r'^start_interview/$',                      'family_info.views.start_interview'),
  (r'^dashboard/$',                            'family_info.views.dashboard'),
  (r'^end_interview/$',                        'family_info.views.end_interview'),
  (r'^help_summary/$',                         'family_info.views.help_summary'),     
  (r'^summary_table/$',                        'family_info.views.summary_table'),     
  (r'^question_list/$',                        'family_info.views.question_list'),    
  (r'^selenium/(?P<task>\w+)/$',               'family_info.views.selenium'),
  (r'^kill/visit/(?P<visit_id>\d+)/$',         'family_info.views.kill_visit'),
  (r'^kill/localstorage/$',                    'family_info.views.kill_localstorage'),
)
