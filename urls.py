from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns(
  '',
                        
  #FAVICON
  (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/site_media/images/favicon.ico'}),
  (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logged_out.html'}),

  # Example:
  # (r'^smilekit/', include('smilekit.foo.urls')),
  ('^accounts/',include('djangowind.urls')),
  (r'^admin/(.*)', admin.site.root),

  #(r'^survey/',include('survey.urls')),
  (r'^tinymce/', include('tinymce.urls')),
  (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
  (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
  (r'^weights/', include('equation_balancer.urls')),
  (r'^collection_tool/', include('collection_tool.urls')),
  (r'^family_info/', include('family_info.urls')),


             
  (r'^logout$', 'django.contrib.auth.views.logout', {'template_name': 'family_info/logged_out.html', 'next_page':'/welcome/?next=/welcome'}),



  #GENERIC WELCOME URL:
  (r'', 'family_info.views.families')

  #LEAVE THIS AT THE END. Otherwise it leads to redirect loops.
  
  #('',  'family_info.views.participants'),
  #('','django.views.generic.simple.redirect_to', {'url':'/welcome/'}),                      
)
