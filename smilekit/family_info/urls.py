from django.conf.urls import patterns
import os.path

media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = patterns(
    '',
    (r'media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': media_root}),
    (r'^families/$', 'smilekit.family_info.views.families'),
    (r'^new_family/$', 'smilekit.family_info.views.new_family'),
    (r'^insert_family/$', 'smilekit.family_info.views.insert_family'),
    (r'^edit_family/(?P<family_id>\d+)/$',
     'smilekit.family_info.views.edit_family'),
    (r'^new_user/$', 'smilekit.family_info.views.new_user'),
    (r'^insert_user/$', 'smilekit.family_info.views.insert_user'),
    (r'^edit_user/(?P<user_id>\d+)/$', 'smilekit.family_info.views.edit_user'),
    (r'^start_interview/$', 'smilekit.family_info.views.start_interview'),
    (r'^dashboard/$', 'smilekit.family_info.views.dashboard'),
    (r'^end_interview/$', 'smilekit.family_info.views.end_interview'),
    (r'^help_summary/$', 'smilekit.family_info.views.help_summary'),
    (r'^summary_table/$', 'smilekit.family_info.views.summary_table'),
    (r'^food_table/$', 'smilekit.family_info.views.food_table'),
    (r'^question_list/$', 'smilekit.family_info.views.question_list'),
    (r'^selenium/(?P<task>\w+)/$', 'smilekit.family_info.views.selenium'),
    (r'^kill/visit/(?P<visit_id>\d+)/$',
     'smilekit.family_info.views.kill_visit'),
    (r'^kill/localstorage/$', 'smilekit.family_info.views.kill_localstorage'),
)
