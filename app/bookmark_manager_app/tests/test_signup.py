from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class SignUpTest(TestCase):
    def setUp(self):
        self.username = 'user4'
        self.password = 'User4Password'

    def test_signup_url(self):
        response = self.client.get("/accounts/signup")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='signup.html')

    def test_signup_view_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='signup.html')

    def test_signup_form(self):
        response = self.client.post(reverse('signup'), data={
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)