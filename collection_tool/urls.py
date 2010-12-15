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
      
      
      (r'risk/language/(?P<language_code>\w+)$', 'collection_tool.views.risk'), 
           
      (r'topics/language/(?P<language_code>\w+)$', 'collection_tool.views.topics'), 
      (r'topic/(?P<topic_id>\d+)/language/(?P<language_code>\w+)$', 'collection_tool.views.topic'), 
      
      (r'goals/language/(?P<language_code>\w+)$', 'collection_tool.views.goals'), 
      
      (r'^goal/(?P<goal_id>\d+)/language/(?P<language_code>\w+)$', 'collection_tool.views.goal'), 
      
      
      (r'planner/goal/(?P<goal_id>\d+)/language/(?P<language_code>\w+)$', 'collection_tool.views.goal_planner'), 
      
      
      


)
