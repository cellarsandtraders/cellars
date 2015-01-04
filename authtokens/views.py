import json
from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError

from authtokens.models import Token
from utils import json_response, token_required


def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            User = get_user_model()
            user = User.objects.create_user(username, None, password)
            token = Token.objects.create(user=user)
        except (ValueError, IndexError, IntegrityError) as e:
            return json_response({
                'error': "Invalid Data: {}".format(e)
            }, status=400)

        return json_response({
            'token': token.token,
            'username': user.username
        }, status=201)

    elif request.method == 'OPTIONS':
        return json_response({})

    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)


def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', None)
        password = data.get('password', None)

        if username is not None and password is not None:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return json_response({
                        'token': token.token,
                        'username': user.username
                    })
                else:
                    return json_response({
                        'error': 'Invalid User'
                    }, status=400)
            else:
                return json_response({
                    'error': 'Invalid Username/Password'
                }, status=400)
        else:
            return json_response({
                'error': 'Invalid Data'
            }, status=400)
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)


@token_required
def logout(request):
    if request.method == 'POST':
        request.token.delete()
        return json_response({
            'status': 'success'
        })
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)


def _error_response(message, status=400):
    return json_response({'error': message}, status=status)
