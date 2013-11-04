from django.conf.urls import patterns
import os.path

media_root = os.path.join(os.path.dirname(__file__), "../media")


urlpatterns = patterns(
    '',
    (r'media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': media_root}),
    (r'configuration/(?P<config_id>\d+)',
     'smilekit.equation_balancer.views.view_config'),
    (r'create', 'smilekit.equation_balancer.views.new_config'),
    (r'save', 'smilekit.equation_balancer.views.save_config'),
    (r'delete/(?P<config_id>\d+)',
     'smilekit.equation_balancer.views.delete_config'),
    (r'import$', 'smilekit.equation_balancer.views.import_config'),
    (r'export/(?P<config_id>\d+)',
     'smilekit.equation_balancer.views.export_config'),
    (r'load$', 'smilekit.equation_balancer.views.load_patient_data'),
    (r'recalculate$', 'smilekit.equation_balancer.views.recalculate'),
    (r'loadquestions', 'smilekit.equation_balancer.views.load_questions'),
    (r'', 'smilekit.equation_balancer.views.index'),
)
