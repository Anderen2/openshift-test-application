import newrelic.agent
newrelic.agent.initialize()
print("Newrelic init #2")

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'web.views.index'),
	url(r'^post$', 'web.views.post'),
	url(r'^api/getlatestpost$', 'web.views.getLatestPost'),
	url(r'^home$', 'web.views.home'),
	url(r'^login$', 'web.views.login'),
	url(r'^logout$', 'web.views.logout'),
	url(r'^signup$', 'web.views.signUp'),
	url(r'^editdatabase$', 'web.views.editDatabase'),
	url(r'^api/removerowfrommodel$', 'web.views.removeRowFromModel'),
	url(r'^api/editrowinmodel$', 'web.views.editRowInModel'),
)
