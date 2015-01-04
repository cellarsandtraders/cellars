from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^api/auth/', include('authtokens.urls')),
    url(r'^api/search/', include('search.urls')),
    url(r'^api/users/', include('users.urls')),
    url(r'^a/', include(admin.site.urls)),
)
