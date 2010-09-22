from django.conf.urls.defaults import *
from django.conf import settings
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
      #(r'temp_html$', 'collection_tool.views.temp_html'),
      
      (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
       
      (r'html_sandbox$', 'collection_tool.views.html_sandbox'), 
      (r'widget_test$', 'collection_tool.views.widget_test'), 
      
      (r'manifest\.cache$',     'collection_tool.views.manifest'),
      
      (r'yes/$', 'collection_tool.views.available_offline'),
  
      (r'online_check$', 'collection_tool.views.online_check'),
  
      
      (r'no/$', 'collection_tool.views.not_available_offline'),

      (r'question/(?P<displayquestion_id>\d+)/language/(?P<language_code>\w+)/$', 'collection_tool.views.question'), 
      
      (r'section/(?P<section_id>\d+)/language/(?P<language_code>\w+)/$', 'collection_tool.views.section'), 
      
      
      (r'video/(?P<video_filename>\w+)/$', 'collection_tool.views.video'), 
      
      
      
      (r'interview_management_login$',                    'collection_tool.views.interview_management_login'), 
      (r'interview_management_participants$',             'collection_tool.views.interview_management_participants'), 
      (r'interview_management_family_assessment$',        'collection_tool.views.interview_management_family_assessment'),
      (r'interview_management_family_information$',       'collection_tool.views.interview_management_family_information'), 
      (r'interview_management_health_worker_information$','collection_tool.views.interview_management_health_worker_information'), 
      (r'interview_management_sync$',                     'collection_tool.views.interview_management_sync'),
      
)

