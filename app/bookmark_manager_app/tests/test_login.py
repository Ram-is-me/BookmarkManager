from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.urls import reverse

class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'user4',
            'password': 'User4Password'}
        User.objects.create_user(**self.credentials)

    def test_login_url(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/login.html')

    def test_signup_view_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/login.html')

    def test_login_form(self):
        response = self.client.post('/accounts/login/', self.credentials, follow=True)      
        self.assertTrue(response.context['user'].is_authenticated)