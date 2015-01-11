import json
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
        return user_details(request, username)

    elif request.method == 'POST':
        return user_update(request, username)


def user_details(request, username):
    user = get_object_or_404(UserProfile, username=username)
    response = serializers.serialize(
        "json", [user], fields=UserProfile.API_FIELDS
    )
    return json_response(response, serialize=False)


@token_required
def user_update(request, username):
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
def collection(request, username, collection):
    if request.method == 'GET':
        return user_collection_list(request, username, collection)

    elif request.method == 'POST':
        return user_collection_update(request, username, collection)

    elif request.method == 'DELETE':
        return user_collection_delete(request, username, collection)


def user_collection_list(request, username, collection):
    user = get_object_or_404(UserProfile, username=username)
    collection = user.cellar if collection == 'cellar' else user.wishlist
    cellar = serializers.serialize("json", collection.all())
    return json_response(cellar, serialize=False)


@token_required
def user_collection_update(request, username, collection):
    user = request.user
    collection = user.cellar if collection == 'cellar' else user.wishlist
    # Do not allow a user to update anyone other than themself
    if user.username != username:
        return json_response({'error': "Forbidden"}, status=403)

    data = json.loads(request.body)
    item, created = collection.get_or_create(pk=data['pk'])
    itemform = CellarItemForm(data, instance=item)
    if not itemform.is_valid():
        return json_response(itemform.errors, status=400)

    itemform.save()
    return json_response({
        'username': username,
        'created': created,
        'item': itemform.cleaned_data,
        'pk': itemform.instance.pk
    })


@token_required
def user_collection_delete(request, username, collection):
    user = request.user
    collection = user.cellar if collection == 'cellar' else user.wishlist
    # Do not allow a user to update anyone other than themself
    if user.username != username:
        return json_response({'error': "Forbidden"}, status=403)

    data = json.loads(request.body)
    item = get_object_or_404(collection, pk=data['pk'])
    if item:
        item.delete()
    return json_response({})
