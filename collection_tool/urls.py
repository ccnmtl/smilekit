from django.conf.urls.defaults import *
from django.conf import settings
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
      #(r'temp_html$', 'collection_tool.views.temp_html'),
      
      (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
       
      (r'html_sandbox$', 'collection_tool.views.html_sandbox'), 
      
      (r'manifest\.cache$',     'collection_tool.views.manifest'),
      
      (r'yes/$', 'collection_tool.views.available_offline'),
      
      (r'no/$', 'collection_tool.views.not_available_offline'),



      (r'question/(?P<displayquestion_id>\d+)/language/(?P<language_code>\w+)/$', 'collection_tool.views.question'), 
)
