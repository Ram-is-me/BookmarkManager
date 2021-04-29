from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class HomePageTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'user4',
            'password': 'User4Password'}
        User.objects.create_user(**self.credentials)

        self.credentials_wrong = {
            'username': 'user4',
            'password': 'user4password'}

    def test_home_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, template_name='registration/login.html')

    def test_home_failure(self):
        response = self.client.post('', self.credentials_wrong, follow=True)      
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, template_name='registration/login.html')

    def test_home_success(self):
        response = self.client.post('', self.credentials, follow=True)      
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, template_name='groups.html')