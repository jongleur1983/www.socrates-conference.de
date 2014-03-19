from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^details.html$', TemplateView.as_view(template_name='details.html'), name='details'),
    url(r'^impressum.html$', TemplateView.as_view(template_name='impressum.html'), name='impressum'),
    url(r'^registration.html$', TemplateView.as_view(template_name='registration.html'), name='registration'),
    url(r'^agenda.html$', TemplateView.as_view(template_name='agenda.html'), name='agenda'),
    url(r'^location.html$', TemplateView.as_view(template_name='location.html'), name='location'),
    url(r'^history.html$', TemplateView.as_view(template_name='history.html'), name='history'),
    url(r'^sponsoring.html$', TemplateView.as_view(template_name='sponsoring.html'), name='sponsoring'),
    url(r'^contact.html$', TemplateView.as_view(template_name='contact.html'), name='contact'),

    url(r'^wiki/', include('wakawaka.urls.authenticated')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^accounts/', include('gatekeeper.urls')),

    url(r'robots.txt', TemplateView.as_view(template_name="robots.txt")),
    
    # use gunicorn to serve static files ... might be changed in later releases
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
