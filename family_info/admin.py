from smilekit.family_info.models import *
from django.contrib import admin

admin.site.register(Family)
admin.site.register(Visit)

class ResponseAdmin(admin.ModelAdmin):
  #search_fields=[ 'dir', ]
  list_display=( 'date_of_response', 'interviewer',\
    'id_of_family', 'question_english', 'answer_english',\
    'config', 'module', 'module_weight', 'question_weight', \
    'answer_weight','score', )
  #fields = [ 'dir']
  #inlines = [HelpUrlInline, HelpBulletPointInline, HelpDefinitionInline]

admin.site.register(Response, ResponseAdmin)




