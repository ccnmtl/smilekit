from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'smilekit.family_info.views.families'),
    (r'^favicon\.ico$',
     RedirectView.as_view(url='/media/images/favicon.ico')),
    (r'^logout/$', 'django.contrib.auth.views.logout',
     {'template_name': 'logged_out.html'}),
    ('^accounts/', include('djangowind.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    (r'^weights/', include('smilekit.equation_balancer.urls')),
    (r'^collection_tool/', include('smilekit.collection_tool.urls')),
    (r'^family_info/', include('smilekit.family_info.urls')),
    (r'^logout$',
     'django.contrib.auth.views.logout',
     {
         'template_name': 'family_info/logged_out.html',
         'next_page': '/?next=/'
     }),
    ('^smoketest/$', include('smoketest.urls')),
)
