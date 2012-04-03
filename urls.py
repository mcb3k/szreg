from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'register.views.index', name='home'),
    # url(r'^szreg/', include('szreg.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^register/$', 'register.views.index'),
	url(r'^register/(?P<event_id>\d+)/$', 'register.views.detail'),
	url(r'^register/(?P<event_id>\d+)/registrationForm/$', 'register.views.registrationForm'),
	url(r'^register/(?P<event_id>\d+)/register/$', 'register.views.register'),
	url(r'^register/(?P<event_id>\d+)/thanks/$', 'register.views.thanks'),    
	url(r'^admin/', include(admin.site.urls)),
)


