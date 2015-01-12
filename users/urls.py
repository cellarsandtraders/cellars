from django.conf.urls import patterns, url


urlpatterns = patterns('users.views',
    url(r'^$', 'user_list', name='user_list'),
    url(r'^activity/$', 'activity', name='activity'),
    url(r'^(?P<username>\w+)/$', 'profile', name='profile'),
    url(r'^(?P<username>\w+)/(?P<collection>[cellar|wishlist]+)/$', 'collection', name='collection'),
    url(r'^(?P<username>\w+)/(?P<action>[(un)?follow]+)/$', 'relationship', name='relationship'),
    url(r'^(?P<username>\w+)/activity/$', 'activity', name='activity'),
)
