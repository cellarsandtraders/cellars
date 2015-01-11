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
        self.assertEqual(response_data[0]['fields']['username'], self.username)

    def test_user_details(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': self.username}))

        self.assertEqual(response.status_code, 200)

        # Read the response data
        response_data = json.loads(response.content)
        self.assertTrue(isinstance(response_data, list))
        self.assertTrue(len(response_data), 1)
        self.assertEqual(response_data[0]['fields']['username'], self.username)

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
