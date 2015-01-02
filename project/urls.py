from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^api/', include('authtokens.urls')),
    url(r'^api/', include('search.urls')),
    url(r'^a/', include(admin.site.urls)),
)
