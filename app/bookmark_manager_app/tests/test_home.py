from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class HomePageTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='user4')
        user.set_password('User4Password')
        user.save()

    def test_home_url(self):
        response = self.client.get('', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/login.html')

    def test_home_failure(self):
        response = self.client.post(reverse('home'), { 'username' : "user4", 'password' : "user4password" })
        self.assertEquals(response.status_code, 302)

    def test_home_success(self):
        response = self.client.post(reverse('home'), { 'username' : "user4", 'password' : "User4Password" })
        self.assertEquals(response.status_code, 302)