from smilekit.family_info.models import *
from django.contrib import admin

admin.site.register(Family)

class VisitAdmin (admin.ModelAdmin):

  list_display=('id', 'start_timestamp', 'end_timestamp', 'interviewer') 
  fields = ( 'end_timestamp', 'families', 'interviewer')

admin.site.register(Visit, VisitAdmin)


class ResponseAdmin(admin.ModelAdmin):
  #search_fields=[ 'dir', ]
  list_display=( 'date_of_response', 'interviewer',\
    'id_of_family', 'question_english', 'answer_english',\
    'config', 'module', 'module_weight', 'question_weight', \
    'answer_weight','score', )

admin.site.register(Response, ResponseAdmin)




