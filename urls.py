from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       # Example:
                       # (r'^smilekit/', include('smilekit.foo.urls')),
                       ('^accounts/',include('djangowind.urls')),
                       (r'^admin/(.*)', admin.site.root),
		       (r'^survey/',include('survey.urls')),
                       (r'^tinymce/', include('tinymce.urls')),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
                       (r'^weights/', include('equation_balancer.urls')),
                       (r'^collection_tool/', include('collection_tool.urls')),
                       (r'^family_info/', include('family_info.urls')),
)
