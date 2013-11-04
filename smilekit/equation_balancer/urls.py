from django.conf.urls import patterns
import os.path

media_root = os.path.join(os.path.dirname(__file__), "../media")


urlpatterns = patterns(
    '',
    (r'media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': media_root}),
    (r'configuration/(?P<config_id>\d+)',
     'equation_balancer.views.view_config'),
    (r'create', 'equation_balancer.views.new_config'),
    (r'save', 'equation_balancer.views.save_config'),
    (r'delete/(?P<config_id>\d+)', 'equation_balancer.views.delete_config'),
    (r'import$', 'equation_balancer.views.import_config'),
    (r'export/(?P<config_id>\d+)', 'equation_balancer.views.export_config'),
    (r'load$', 'equation_balancer.views.load_patient_data'),
    (r'recalculate$', 'equation_balancer.views.recalculate'),
    (r'loadquestions', 'equation_balancer.views.load_questions'),
    (r'', 'equation_balancer.views.index'),
)
