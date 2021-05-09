from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime
from bookmark_manager_app import models

class CreateAndDeleteTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user4', password='User4Password')
        user.save()
        models.User.objects.create(name='user4')
        self.client.post(reverse('login'), { 'username' : "user4", 'password' : "User4Password" })

    def test_create_group(self):
        response = self.client.post(reverse('create_group', args=('user4', )), {'groupname' : "group41"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(models.Group.objects.filter(name="group41").exists())
        self.client.post(reverse('delete_group', args=('user4', )), {'deletegroupname' : "group41"})

    def test_create_tag(self):
        response = self.client.post(reverse('create_tag', args=('user4', )), {'tagname' : "tag41"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(models.Tag.objects.filter(name="tag41").exists())
        self.client.post(reverse('delete_tag', args=('user4', )), {'deletetagname' : "tag41"})

    def test_delete_group(self):
        self.client.post(reverse('create_group', args=('user4', )), {'groupname' : "group41"})
        response = self.client.post(reverse('delete_group', args=('user4', )), {'deletegroupname' : "group41"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(models.Group.objects.filter(name="group41").exists())

    def test_delete_tag(self):
        self.client.post(reverse('create_tag', args=('user4', )), {'tagname' : "tag41"})
        response = self.client.post(reverse('delete_tag', args=('user4', )), {'deletetagname' : "tag41"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(models.Tag.objects.filter(name="tag41").exists())

    def test_delete_reminder(self):
        self.client.post(reverse('create_group', args=('user4', )), {'groupname' : "group41"})
        self.client.post(reverse('add_bookmark', args=('user4', models.Group.objects.get(name="group41").id, )), {'custom_name' : "bkmark1", 'custom_note' : "bkamrk1 note", 'url' : "https://youtube.com"})
        self.client.post(reverse('addreminder', args=('user4', models.Bookmark.objects.get(custom_name="bkmark1").id, )), {'name' : "reminder1", 'description' : "reminder1 description", 'reminder_time' : timezone.now()+datetime.timedelta(days=1)})
        response = self.client.get(reverse('delete_reminder', args=('user4', "reminder1", )))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(models.Reminder.objects.filter(name="reminder1").exists())