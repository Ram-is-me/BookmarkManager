from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime
from bookmark_manager_app import models

class EditBookmarkTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user4', password='User4Password')
        user.save()
        models.User.objects.create(name='user4')
        self.client.post(reverse('login'), { 'username' : "user4", 'password' : "User4Password" })

    def test_edit_bookmark(self):
        self.client.post(reverse('create_group', args=('user4', )), {'groupname' : "group41"})
        self.client.post(reverse('add_bookmark', args=('user4', models.Group.objects.get(name="group41").id, )), {'custom_name' : "bkmark1", 'custom_note' : "bkmark1 note", 'url' : "https://youtube.com"})
        response = self.client.post(reverse('view_bookmark', args=('user4', models.Bookmark.objects.get(custom_name="bkmark1").id, )), {'custom_name' : "bkmark1_mod", 'custom_note' : "bkmark1 note", 'url' : "https://google.com"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(models.Bookmark.objects.filter(custom_name="bkmark1_mod").exists())

    def test_add_reminder(self):
        self.client.post(reverse('create_group', args=('user4', )), {'groupname' : "group41"})
        self.client.post(reverse('add_bookmark', args=('user4', models.Group.objects.get(name="group41").id, )), {'custom_name' : "bkmark1", 'custom_note' : "bkamrk1 note", 'url' : "https://youtube.com"})
        response = self.client.post(reverse('addreminder', args=('user4', models.Bookmark.objects.get(custom_name="bkmark1").id, )), {'name' : "reminder1", 'description' : "reminder1 description", 'reminder_time' : timezone.now()+datetime.timedelta(days=1)})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.Reminder.objects.filter(name="reminder1").exists())