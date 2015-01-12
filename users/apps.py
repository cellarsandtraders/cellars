from django.apps import AppConfig
from actstream import registry


class UsersBackendConfig(AppConfig):
    name = 'users'

    def ready(self):
        registry.register(self.get_model('UserProfile'))
        registry.register(self.get_model('CellarItem'))
