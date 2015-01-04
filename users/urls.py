from django.conf.urls import patterns, url


urlpatterns = patterns('users.views',
    url(r'^$', 'list_users', name='list'),
    url(r'^(?P<username>\w+)$', 'profile', name='profile'),
)
