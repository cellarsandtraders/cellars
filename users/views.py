import json
from actstream import action
from actstream.actions import (
    follow as follow_action,
    unfollow as unfollow_action
)
from actstream.models import Action, user_stream
from django.core import serializers
from django.shortcuts import get_object_or_404

from utils import json_response, endpoint, token_required
from users.models import UserProfile
from users.forms import CellarItemForm, UserProfileForm


@endpoint
def user_list(request):
    if request.method == 'GET':
        users = serializers.serialize(
            "json", UserProfile.objects.all(), fields=UserProfile.API_FIELDS
        )
        return json_response(users, serialize=False)


@endpoint
def profile(request, username):
    if request.method == 'GET':
        return _user_details(request, username)

    elif request.method == 'POST':
        return _user_update(request, username)


def _user_details(request, username):
    user = get_object_or_404(UserProfile, username=username)
    response = serializers.serialize(
        "json", [user], fields=UserProfile.API_FIELDS
    )
    return json_response(response, serialize=False)


@token_required
def _user_update(request, username):
    user = request.user
    # Do not allow a user to update anyone other than themself
    if user.username != username:
        return json_response({'error': "Forbidden"}, status=403)

    data = json.loads(request.body)
    userform = UserProfileForm(data, instance=user)
    if not userform.is_valid():
        return json_response(userform.errors, status=400)

    userform.save()
    return json_response(userform.cleaned_data)


@endpoint
def collection(request, username, collection, item_id=None):
    if request.method == 'GET':
        return _user_collection_list(request, username, collection)

    elif request.method == 'POST':
        return _user_collection_update(request, username, collection)

    elif request.method == 'DELETE' and item_id:
        return _user_collection_delete(request, username, collection, item_id)


def _user_collection_list(request, username, collection):
    user = get_object_or_404(UserProfile, username=username)
    collection = user.cellar if collection == 'cellar' else user.wishlist
    cellar = serializers.serialize("json", collection.all())
    return json_response(cellar, serialize=False)


@token_required
def _user_collection_update(request, username, collection_type):
    user = request.user
    collection = user.cellar if collection_type == 'cellar' else user.wishlist
    # Do not allow a user to update anyone other than themself
    if user.username != username:
        return json_response({'error': "Forbidden"}, status=403)

    data = json.loads(request.body)
    item, created = collection.get_or_create(pk=data['pk'])
    itemform = CellarItemForm(data, instance=item)
    if not itemform.is_valid():
        return json_response(itemform.errors, status=400)

    itemform.save()
    action.send(
        user, verb='added', action_object=item,
        collection=collection_type, beer_id=item.pk
    )

    return json_response({
        'username': username,
        'created': created,
        'item': itemform.cleaned_data,
        'pk': itemform.instance.pk
    })


@token_required
def _user_collection_delete(request, username, collection_type, item_id):
    user = request.user
    collection = user.cellar if collection_type == 'cellar' else user.wishlist
    # Do not allow a user to update anyone other than themself
    if user.username != username:
        return json_response({'error': "Forbidden"}, status=403)

    item = get_object_or_404(collection, pk=item_id)
    if item:
        item.delete()
        action.send(
            user, verb='removed', action_object=item,
            collection=collection_type, beer_id=item.pk
        )
    return json_response({})


@token_required
def relationship(request, username, action):
    if request.method == 'GET':
        user = UserProfile.objects.get(username__exact=username)
        if action == 'follow':
            follow_action(request.user, user)
        elif action == 'unfollow':
            unfollow_action(request.user, user)
        else:
            return
        return json_response({})


def activity(request, username=None):
    if request.method == 'GET':
        if username:
            user = get_object_or_404(UserProfile, username=username)
            stream = []
            for action in user_stream(user, with_user_activity=True):
                stream.append(str(action))
        else:
            stream = [str(action) for action in Action.objects.all()[:50]]

        return json_response(stream)
