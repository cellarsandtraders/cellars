from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^register/$', 'authtokens.views.register', name='register'),
    url(r'^login/$', 'authtokens.views.login', name='login'),
    url(r'^logout/$', 'authtokens.views.logout', name='logout'),
)
