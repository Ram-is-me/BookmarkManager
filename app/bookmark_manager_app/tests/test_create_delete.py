from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class CreateAndDeleteTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user4')
        user.set_password('User4Password')
        user.save()
        self.client.post(reverse('home'), { 'username' : "user4", 'password' : "User4Password" })

    def test_create_group(self):
        response = self.client.post(reverse('groups', args=('user4', )), {'groupname' : "group41"})
        self.assertEqual(response.status_code, 302)

    def test_create_tag(self):
        response = self.client.post(reverse('groups', args=('user4', )), {'tagname' : "tag41"})
        self.assertEqual(response.status_code, 302)

    def test_delete_group(self):
        response = self.client.post(reverse('groups', args=('user4', )), {'deletegroupname' : "group41"})
        self.assertEqual(response.status_code, 302)

    def test_delete_tag(self):
        response = self.client.post(reverse('groups', args=('user4', )), {'deletetagname' : "tag41"})
        self.assertEqual(response.status_code, 302)

    # def test_create_duplicate_group(self):
    #     self.client.post(reverse('groups', args=('user4', )), {'groupname' : "group41"})
    #     response = self.client.post(reverse('groups', args=('user4', )), {'groupname' : "group41"})
    #     self.assertEqual(response.status_code, 403)
