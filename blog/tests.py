from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post,Category
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PostTests(APITestCase):

    def test_view_ports(self):

        url = reverse('blogapi:listcreate')

        response = self.client.get(url,format='json')

        self.assertEqual(response.status_code,status.HTTP_200_OK)