from django.conf.urls.defaults import *
from django.conf import settings
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
      
      (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
      (r'widget_test$', 'collection_tool.views.widget_test'), 
      (r'manifest\.cache$',     'collection_tool.views.manifest'),
      
      
      
      (r'question/(?P<displayquestion_id>\d+)/language/(?P<language_code>\w+)$', 'collection_tool.views.question'), 
      (r'section/(?P<section_id>\d+)/language/(?P<language_code>\w+)$', 'collection_tool.views.section'), 
      (r'video/(?P<video_filename>\w+)$', 'collection_tool.views.video'), 

      #(r'html_sandbox$', 'collection_tool.views.html_sandbox'), 
      #(r'yes/$', 'collection_tool.views.available_offline'),
      #(r'no/$', 'collection_tool.views.not_available_offline'),
      #(r'online_check$', 'collection_tool.views.online_check'),
      

)

