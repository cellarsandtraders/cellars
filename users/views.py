from django.core import serializers

from utils import json_response, endpoint
from users.models import UserProfile


@endpoint
def list_users(request):
    if request.method == 'GET':
        users = serializers.serialize(
            "json", UserProfile.objects.all(), fields=UserProfile.API_FIELDS
        )
        return json_response(users, serialize=False)


@endpoint
def profile(request, username=None):
    if request.method == 'GET' and username is not None:
        user = UserProfile.objects.filter(username=username)
        response = serializers.serialize(
            "json", user, fields=UserProfile.API_FIELDS
        )
        return json_response(response, serialize=False)

    elif request.method == 'POST':
        return json_response({})
