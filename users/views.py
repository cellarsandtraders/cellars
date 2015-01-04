from django.core import serializers
from django.http import HttpResponse

from utils import json_response
from users.models import UserProfile


def list_users(request):
    if request.method == 'GET':
        users = serializers.serialize(
            "json", UserProfile.objects.all(), fields=UserProfile.API_FIELDS
        )
        return json_response(users, serialize=False)

    elif request.method == 'OPTIONS':
        return json_response({})

    else:
        return json_response({'error': "Bad Request"}, status=400)


def profile(request):
    if request.method == 'GET':
        return _get_user()

    elif request.method == 'POST':
        return _update_user()

    elif request.method == 'OPTIONS':
        return json_response({})

    else:
        return json_response({'error': "Bad Request"}, status=400)


def _get_user(request):
    return json_response({})


def _update_user(request):
    return json_response({})
