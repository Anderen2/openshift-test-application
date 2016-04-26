from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'web.views.index'),
	url(r'^post$', 'web.views.post'),
	url(r'^api/getlatestpost$', 'web.views.getLatestPost'),
	url(r'^login$', 'web.views.login'),
	url(r'^logout$', 'web.views.logout'),
	url(r'^signup$', 'web.views.signUp'),
	url(r'^displayDatabase$', 'web.views.displayDatabase'),
)
