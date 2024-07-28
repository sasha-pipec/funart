from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from api.factories.theme import ThemeFactory
from api.factories.user import UserFactory


class ThemeListTests(APITestCase):
    def setUp(self):
        self.themes = ThemeFactory.create_batch(10)
        self.user = UserFactory.create_batch(1)[0]
        Token.objects.create(user=self.user)

    def test_status_authorization_and_len_response(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = self.client.get(reverse('theme_list_create'),
                                   {'type': 'recommended'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['themes']), 0)

    def test_count_objects_with_pagination(self):
        response = self.client.get(reverse('theme_list_create'), {'page': 1, 'per_page': 8})
        self.assertEqual(len(response.data['themes']), 8)

        response2 = self.client.get(reverse('theme_list_create'), {'page': 2, 'per_page': 8})
        self.assertEqual(len(response2.data['themes']), 2)

        response3 = self.client.get(reverse('theme_list_create'), {'page': 3, 'per_page': 2})
        self.assertEqual(len(response3.data['themes']), 2)

        response3 = self.client.get(reverse('theme_list_create'), {'page': 4, 'per_page': 3})
        self.assertEqual(len(response3.data['themes']), 1)

    def test_comparing_incoming_objects(self):
        response = self.client.get(reverse('theme_list_create'), {'page': 1, 'per_page': 10})
        response_data = [
            (('id', i['id']), ('name', i['name']), ('description', i['description']), ('rating', i['rating'])) for i in
            response.data['themes']]
        themes_data = [(('id', i.id), ('name', i.name), ('description', i.description), ('rating', i.rating)) for i in
                       self.themes]

        for theme in themes_data:
            self.assertIn(theme, response_data)
