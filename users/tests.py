import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from authtokens.models import Token
from users.models import UserProfile


class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'test'
        self.password = '123'
        self.user = UserProfile.objects.create_user(
            self.username, None, self.password)
        self.token = Token.objects.create(user=self.user)

    def test_user_list(self):
        response = self.client.get(
            reverse('user_list'))

        self.assertEqual(response.status_code, 200)

        # Read the response data
        response_data = json.loads(response.content)
        self.assertTrue(isinstance(response_data, list))
        self.assertTrue(len(response_data), 1)
        self.assertEqual(response_data[0]['username'], self.username)

    def test_user_details(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': self.username}))

        self.assertEqual(response.status_code, 200)

        # Read the response data
        response_data = json.loads(response.content)
        self.assertTrue(isinstance(response_data, dict))
        self.assertTrue(len(response_data), 1)
        self.assertEqual(response_data['username'], self.username)

    def test_user_not_found(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': 'not_a_user'}))
        self.assertEqual(response.status_code, 404)

    def test_user_update_success(self):
        new_email = 'email@example.com'
        self.assertEqual(UserProfile.objects.filter(email=new_email).count(), 0)
        new_data = {
            'username': self.username,
            'first_name': "Test",
            'last_name': "User",
            'email': new_email
        }
        response = self.client.post(
            reverse('profile', kwargs={'username': self.username}),
            json.dumps(new_data),
            HTTP_AUTHORIZATION='Token {}'.format(self.token.token),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # Read the response data
        response_data = json.loads(response.content)
        self.assertTrue(isinstance(response_data, dict))
        self.assertEqual(response_data['username'], self.username)
        self.assertEqual(response_data['email'], new_email)

        self.assertEqual(UserProfile.objects.filter(email=new_email).count(), 1)

    def test_user_update_address(self):
        self.assertEqual(UserProfile.objects.filter(address="address").count(), 0)
        new_data = {
            'username': self.user.username,
            'first_name': "Test",
            'last_name': "User",
            'email': "test@example.com",
            "address": "address",
            "address2": "address2",
            "city": "city",
            "state": "IL",  # Must be valid state
            "zipcode": "60647",  # Must be valid postal code
        }
        response = self.client.post(
            reverse('profile', kwargs={'username': self.username}),
            json.dumps(new_data),
            HTTP_AUTHORIZATION='Token {}'.format(self.token.token),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # Read the response data
        response_data = json.loads(response.content)
        self.assertTrue(isinstance(response_data, dict))
        self.assertEqual(response_data['username'], self.username)
        self.assertEqual(response_data['address'], "address")
        self.assertEqual(response_data['address2'], "address2")
        self.assertEqual(response_data['city'], "city")
        self.assertEqual(response_data['state'], "IL")
        self.assertEqual(response_data['zipcode'], "60647")

        self.assertEqual(UserProfile.objects.filter(address="address").count(), 1)

    def test_user_update_validation_error(self):
        new_data = {
            'username': self.username,
        }
        response = self.client.post(
            reverse('profile', kwargs={'username': self.username}),
            json.dumps(new_data),
            HTTP_AUTHORIZATION='Token {}'.format(self.token.token),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

        # Read the response data
        response_data = json.loads(response.content)
        self.assertTrue(isinstance(response_data, dict))
        # The response indicated the following keys not present
        self.assertTrue('username' not in response_data)
        self.assertTrue('first_name' in response_data)
        self.assertTrue('last_name' in response_data)
        self.assertTrue('email' in response_data)

    def test_user_cannot_edit_another_user(self):
        response = self.client.post(
            reverse('profile', kwargs={'username': 'not_me'}),
            json.dumps({}),
            HTTP_AUTHORIZATION='Token {}'.format(self.token.token),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)


class UserCollectionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'test'
        self.password = '123'
        self.user = UserProfile.objects.create_user(
            self.username, None, self.password)
        self.token = Token.objects.create(user=self.user)
        self.item = {
            "beer_id": "sHgBrJ",
            "beer_name": "Big Hugs",
            "brewery_id": "lZfiot",
            "brewery_name": "Half Acre Beer Company",
            "style": "American-Style Imperial Stout",
            "abv": "10",
            "year": "2012",
            "quantity": "1",
            "willing_to_trade": False,
            "label": "https://s3.amazonaws.com/brewerydbapi/beer/sHgBrJ/upload_9PO5av-large.png"
        }
        self.collection = 'cellar'

    def test_user_list(self):
        self.user.cellar.create(**self.item)
        response = self.client.get(reverse('collection', kwargs={
            'username': self.username, 'collection': self.collection
        }))

        self.assertEqual(response.status_code, 200)

        # Read the response data
        response_data = json.loads(response.content)
        self.assertTrue(isinstance(response_data, list))
        self.assertTrue(len(response_data), 1)
        self.assertEqual(response_data[0]['beer_name'], u'Big Hugs')

    def test_user_collection_update(self):
        ## Add an item to an empty collection
        self.assertEqual(self.user.cellar.all().count(), 0)
        self.item.update({'pk': None})
        response = self.client.post(
            reverse('collection', kwargs={
                'username': self.username, 'collection': self.collection
            }),
            json.dumps(self.item),
            HTTP_AUTHORIZATION='Token {}'.format(self.token.token),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # Read the response data
        response_data = json.loads(response.content)
        self.assertTrue(isinstance(response_data, dict))
        self.assertEqual(response_data['item']['beer_name'], u"Big Hugs")
        self.assertEqual(self.user.cellar.all().count(), 1)

        ## Update an existing item in a collection
        self.item.update({'pk': response_data['pk'], 'beer_name': "Little Hugs"})
        response = self.client.post(
            reverse('collection', kwargs={
                'username': self.username, 'collection': self.collection
            }),
            json.dumps(self.item),
            HTTP_AUTHORIZATION='Token {}'.format(self.token.token),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # Read the response data
        response_data = json.loads(response.content)
        self.assertTrue(isinstance(response_data, dict))
        self.assertEqual(response_data['item']['beer_name'], u"Little Hugs")
        self.assertEqual(self.user.cellar.all().count(), 1)

    def test_user_cannot_edit_another_users_collection(self):
        response = self.client.post(
            reverse('collection', kwargs={
                'username': 'not_me', 'collection': self.collection
            }),
            json.dumps(self.item),
            HTTP_AUTHORIZATION='Token {}'.format(self.token.token),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_user_collection_delete_item(self):
        item = self.user.cellar.create(**self.item)
        self.assertEqual(self.user.cellar.all().count(), 1)
        response = self.client.delete(
            reverse('collection', kwargs={
                'username': self.username,
                'collection': self.collection,
                'item_id': item.pk
            }),
            HTTP_AUTHORIZATION='Token {}'.format(self.token.token),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.cellar.all().count(), 0)

    def test_user_collection_delete_invalid_item(self):
        response = self.client.delete(
            reverse('collection', kwargs={
                'username': self.username,
                'collection': self.collection,
                'item_id': 999
            }),
            HTTP_AUTHORIZATION='Token {}'.format(self.token.token),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(
            reverse('collection', kwargs={
                'username': 'not_mine',
                'collection': self.collection,
                'item_id': 999
            }),
            HTTP_AUTHORIZATION='Token {}'.format(self.token.token),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
