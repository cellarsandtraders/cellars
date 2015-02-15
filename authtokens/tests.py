import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from authtokens.models import Token


class RegisterTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_successful_registration(self):
        # Create the request to register a new user
        data = {'username': 'testing', 'password': '123'}
        response = self.client.post(
            reverse('register'),
            json.dumps(data),
            content_type='application/json'
        )

        # Assert the request was successful
        self.assertEqual(response.status_code, 201)

        # Read the response data
        response_data = json.loads(response.content)
        response_token = response_data['token']
        response_user = response_data['user']

        # Assert the response token matches the user record in the DB
        self.assertTrue('username' in response_user)
        user = get_user_model().objects.get(username=response_user['username'])
        authtoken = user.authtoken.get()
        self.assertEqual(authtoken.token, response_token)
        self.assertEqual(user.to_json(), response_user)

    def test_repeat_registration(self):
        # Create the request to register a new user
        data = {'username': 'testing', 'password': '123'}
        response = self.client.post(
            reverse('register'),
            json.dumps(data),
            content_type='application/json'
        )

        # Assert the request was successful
        self.assertEqual(response.status_code, 201)

        # Attempt to register with the same credentials
        response = self.client.post(
            reverse('register'),
            json.dumps(data),
            content_type='application/json'
        )

        # Assert the request was not successful
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in json.loads(response.content))

    def test_bad_request(self):
        # Create the request to register a new user
        response = self.client.post(reverse('register'), "",
            content_type='application/json')

        # Assert the request failed with error
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in json.loads(response.content))


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = '123'
        self.user = get_user_model().objects.create_user(self.username, None, self.password)
        self.token = Token.objects.create(user=self.user)

    def test_successful_login(self):
        # Login with existing credentials
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(
            reverse('login'),
            json.dumps(data),
            content_type='application/json'
        )

        # Assert the request was successful
        self.assertEqual(response.status_code, 200)

        # Read the response data
        response_data = json.loads(response.content)
        response_token = response_data['token']
        response_user = response_data['user']

        # Assert the response token matches the user record in the DB
        self.assertTrue('username' in response_user)
        user = get_user_model().objects.get(username=response_user['username'])
        authtoken = user.authtoken.get()
        self.assertEqual(authtoken.token, response_token)
        self.assertEqual(user.to_json(), response_user)

    def test_repeat_login(self):
        # Login with existing credentials
        data = {'username': self.username, 'password': self.password}
        response1 = self.client.post(
            reverse('login'),
            json.dumps(data),
            content_type='application/json'
        )

        # Assert the request was successful
        self.assertEqual(response1.status_code, 200)

        # Attempt to login again with the same credentials
        data = {'username': self.username, 'password': self.password}
        response2 = self.client.post(
            reverse('login'),
            json.dumps(data),
            content_type='application/json'
        )

        # Assert the request was successful
        self.assertEqual(response2.status_code, 200)

        # Assert we have the same token
        token1 = json.loads(response1.content)['token']
        token2 = json.loads(response2.content)['token']
        self.assertEqual(token1, token2)

    def test_bad_request(self):
        # Login with invalid
        response = self.client.post(reverse('login'), "{}",
            content_type='application/json')

        # Assert the request failed with error
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in json.loads(response.content))

    def test_bad_credentials(self):
        # Login with invalid
        bad_credentials = {'username': 'nope', 'password': 'nope'}
        response = self.client.post(
            reverse('login'),
            json.dumps(bad_credentials),
            content_type='application/json'
        )

        # Assert the request failed with error
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in json.loads(response.content))

    def test_login_logout(self):
        # Create the request to register a new user
        data = {'username': self.username, 'password': self.password}
        response1 = self.client.post(
            reverse('login'),
            json.dumps(data),
            content_type='application/json'
        )

        # Assert the request was successful
        self.assertEqual(response1.status_code, 200)

        # Attempt to login again with the same credentials
        data = {'username': self.username, 'password': self.password}
        response2 = self.client.post(
            reverse('login'),
            json.dumps(data),
            content_type='application/json'
        )

        # Assert the request was successful
        self.assertEqual(response2.status_code, 200)

        # Assert we have the same token
        token1 = json.loads(response1.content)['token']
        token2 = json.loads(response2.content)['token']
        self.assertEqual(token1, token2)
