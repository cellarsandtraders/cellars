from django.conf.urls import patterns, url


urlpatterns = patterns('users.views',
    url(r'^$', 'user_list', name='user_list'),
    url(r'^(?P<username>\w+)/$', 'profile', name='profile'),
)
