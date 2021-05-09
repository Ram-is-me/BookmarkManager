from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from bookmark_manager_app import models

class AddBookmarkTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user4', password='User4Password')
        user.save()
        models.User.objects.create(name='user4')
        self.client.post(reverse('login'), { 'username' : "user4", 'password' : "User4Password" })

    def test_add_bookmark(self):
        self.client.post(reverse('create_group', args=('user4', )), {'groupname' : "group41"})
        response = self.client.post(reverse('add_bookmark', args=('user4', models.Group.objects.get(name="group41").id, )), {'custom_name' : "bkmark1", 'custom_note' : "bkamrk1 note", 'url' : "https://youtube.com"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.Bookmark.objects.filter(custom_name="bkmark1").exists())