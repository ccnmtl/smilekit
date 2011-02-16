from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns(
  '',                  
  (r'^$', 'family_info.views.families'),
  (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/site_media/images/favicon.ico'}),
  (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logged_out.html'}),
  ('^accounts/',include('djangowind.urls')),
  (r'^admin/(.*)', admin.site.root),
  (r'^tinymce/', include('tinymce.urls')),
  (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
  (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
  (r'^weights/', include('equation_balancer.urls')),
  (r'^collection_tool/', include('collection_tool.urls')),
  (r'^family_info/', include('family_info.urls')),
  (r'^logout$', 'django.contrib.auth.views.logout',
    {
      'template_name': 'family_info/logged_out.html',
      'next_page':'/?next=/'
    }
  ),
)
