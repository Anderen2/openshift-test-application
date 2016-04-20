from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'web.views.index'),
	url(r'^post/$', 'web.views.post'),
	url(r'^login/$', 'web.views.login'),

	url(r'^admin/', include(admin.site.urls)),
)
