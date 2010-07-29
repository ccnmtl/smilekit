from django.conf.urls.defaults import *
from django.conf import settings
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
      (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
      #(r'temp_html$', 'collection_tool.views.temp_html'),
                        
      (r'question/(?P<question_id>\d+)/language/(?P<language_code>\w+)/$', 'collection_tool.views.question'), 
                        
)
