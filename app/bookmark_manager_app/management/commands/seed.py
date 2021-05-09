from django.contrib.auth.models import User
# from ...models import *
from bookmark_manager_app import models

from datetime import datetime

from django.utils import timezone
from django.http import HttpResponse
import datetime

from django.core.management.base import BaseCommand
import random

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        init(self)
        self.stdout.write('done.')

def init(self):
    
    list_of_user_objects = []
    list_of_user_tags = []
    list_of_user_groups = []
    
    for i in range(0,50):
        user = User.objects.create(username="user"+str(i))
        user.set_password("User"+str(i)+"Password")
        user.save()
        
        userm = models.User(name = "user"+str(i))
        userm.save()
        list_of_user_objects.append(userm)
    
    # user = User.objects.create(username="user1")
    # user.set_password("User1Password")
    # user.save()
    # user = User.objects.create(username="user2")
    # user.set_password("User2Password")
    # user.save()
    # user = User.objects.create(username="user3")
    # user.set_password("User3Password")
    # user.save()
    
    # user1 = models.User(name="user1")
    # user1.save()
    # user2 = models.User(name="user2")
    # user2.save()
    # user2 = models.User(name="user3")
    # user2.save()
    
    for user in list_of_user_objects:
        tag1 = models.Tag(name="tag1", creator=user, date_of_creation=timezone.now())
        tag1.save()
        tag2 = models.Tag(name="tag2", creator=user, date_of_creation=timezone.now())
        tag2.save()
        tag3 = models.Tag(name="tag3", creator=user, date_of_creation=timezone.now())
        tag3.save()
        tag4 = models.Tag(name="tag4", creator=user, date_of_creation=timezone.now())
        tag4.save()
        
        list_of_user_tags.append(tag1)
        list_of_user_tags.append(tag2)
        list_of_user_tags.append(tag3)
        list_of_user_tags.append(tag4)
        
        group1 = models.Group(name="group1", creator=user, date_of_creation=timezone.now())
        group1.save()
        group2 = models.Group(name="group2", creator=user, date_of_creation=timezone.now())
        group2.save()
        group3 = models.Group(name="group3", creator=user, date_of_creation=timezone.now())
        group3.save()
        group4 = models.Group(name="group4", creator=user, date_of_creation=timezone.now())
        group4.save()
        
        list_of_user_groups.append(group1)
        list_of_user_groups.append(group2)
        list_of_user_groups.append(group3)
        list_of_user_groups.append(group4)
        
        bkmark1 = models.Bookmark(custom_name="bkmark1", url="www.google.com", creator=user, group=group1, date_of_creation= timezone.now())
        bkmark1.save()
        
        bkmark2 = models.Bookmark(custom_name="bkmark2", url="www.google.com", creator=user, group=group1, date_of_creation= timezone.now())
        bkmark2.save()
        
        bkmark3 = models.Bookmark(custom_name="bkmark3", url="www.google.com", creator=user, group=group2, date_of_creation= timezone.now())
        bkmark3.save()
        
        bkmark4 = models.Bookmark(custom_name="bkmark4", url="www.google.com", creator=user, group=group2, date_of_creation= timezone.now())
        bkmark4.save()

        bkmark5 = models.Bookmark(custom_name="bkmark5", url="www.google.com", creator=user, group=group3, date_of_creation= timezone.now())
        bkmark5.save()

        bkmark6 = models.Bookmark(custom_name="bkmark6", url="www.google.com", creator=user, group=group3, date_of_creation= timezone.now())
        bkmark6.save()

        bkmark7 = models.Bookmark(custom_name="bkmark7", url="www.google.com", creator=user, group=group4, date_of_creation= timezone.now())
        bkmark7.save()

        bkmark8 = models.Bookmark(custom_name="bkmark8", url="www.google.com", creator=user, group=group4, date_of_creation= timezone.now())
        bkmark8.save()

        
        bkmark1.list_of_tags.add(tag1)
        bkmark1.list_of_tags.add(tag2)
        bkmark1.save()
        
        bkmark2.list_of_tags.add(tag2)
        bkmark2.list_of_tags.add(tag3)
        bkmark2.save()
        
        
        bkmark3.list_of_tags.add(tag3)
        bkmark3.list_of_tags.add(tag4)
        bkmark3.save()
        
        
        bkmark4.list_of_tags.add(tag4)
        bkmark4.list_of_tags.add(tag1)
        bkmark4.save()
        
        
        bkmark5.list_of_tags.add(tag1)
        bkmark5.list_of_tags.add(tag3)
        bkmark5.save()
        
        
        bkmark6.list_of_tags.add(tag1)
        bkmark6.list_of_tags.add(tag2)
        bkmark6.list_of_tags.add(tag3)
        bkmark6.save()
        
        bkmark7.list_of_tags.add(tag1)
        bkmark7.list_of_tags.add(tag3)
        bkmark7.list_of_tags.add(tag4)
        bkmark7.save()
        
        bkmark8.list_of_tags.add(tag1)
        bkmark8.list_of_tags.add(tag2)
        bkmark8.list_of_tags.add(tag3)
        bkmark8.list_of_tags.add(tag4)
        bkmark8.save()
        
        reminder1 = models.Reminder(name="reminder1", creator=user, bookmark=bkmark1, reminder_time=timezone.now()+datetime.timedelta(days=1), time_of_creation=timezone.now())
        reminder1.save()
        reminder2 = models.Reminder(name="reminder2", creator=user, bookmark=bkmark8, reminder_time=timezone.now()+datetime.timedelta(days=20), time_of_creation=timezone.now())
        reminder2.save()
        
        
    # bkmark11 = models.Bookmark(custom_name="bkmark11", url="http://bkmark11.com", creator=user1, group=group11, date_of_creation=timezone.now())

    # tag11 = models.Tag(name="tag11", creator=user1, date_of_creation=timezone.now())
    # tag11.save()
    # tag12 = models.Tag(name="tag12", creator=user1, date_of_creation=timezone.now())
    # tag12.save()
    # tag21 = models.Tag(name="tag21", creator=user2, date_of_creation=timezone.now())
    # tag21.save()
    # tag22 = models.Tag(name="tag22", creator=user2, date_of_creation=timezone.now())
    # tag22.save()

    # group11 = models.Group(name="group11", creator=user1, date_of_creation=timezone.now())
    # group11.save()
    # group12 = models.Group(name="group12", creator=user1, date_of_creation=timezone.now())
    # group12.save()
    # group21 = models.Group(name="group21", creator=user2, date_of_creation=timezone.now())
    # group21.save()
    # group22 = models.Group(name="group22", creator=user2, date_of_creation=timezone.now())
    # group22.save()

    # bkmark11 = models.Bookmark(custom_name="bkmark11", url="http://bkmark11.com", creator=user1, group=group11, date_of_creation=timezone.now())
    # bkmark11.save()
    # bkmark12 = models.Bookmark(custom_name="bkmark12", url="http://bkmark12.com", creator=user1, group=group11, date_of_creation=timezone.now())
    # bkmark12.save()
    # bkmark13 = models.Bookmark(custom_name="bkmark13", url="http://bkmark13.com", creator=user1, group=group12, date_of_creation=timezone.now())
    # bkmark13.save()
    # bkmark14 = models.Bookmark(custom_name="bkmark14", url="http://bkmark14.com", creator=user1, group=group12, date_of_creation=timezone.now())
    # bkmark14.save()
    # bkmark21 = models.Bookmark(custom_name="bkmark21", url="http://bkmark21.com", creator=user2, group=group21, date_of_creation=timezone.now())
    # bkmark21.save()
    # bkmark22 = models.Bookmark(custom_name="bkmark22", url="http://bkmark22.com", creator=user2, group=group21, date_of_creation=timezone.now())
    # bkmark22.save()
    # bkmark23 = models.Bookmark(custom_name="bkmark23", url="http://bkmark23.com", creator=user2, group=group22, date_of_creation=timezone.now())
    # bkmark23.save()
    # bkmark24 = models.Bookmark(custom_name="bkmark24", url="http://bkmark24.com", creator=user2, group=group22, date_of_creation=timezone.now())
    # bkmark24.save()

    # bkmark11.list_of_tags.add(tag11)
    # bkmark11.save()
    # bkmark12.list_of_tags.add(tag11, tag12)
    # bkmark12.save()
    # bkmark13.list_of_tags.add(tag12)
    # bkmark13.save()
    # bkmark14.list_of_tags.add(tag11, tag12)
    # bkmark14.save()
    # bkmark21.list_of_tags.add(tag21)
    # bkmark21.save()
    # bkmark22.list_of_tags.add(tag21, tag22)
    # bkmark22.save()
    # bkmark23.list_of_tags.add(tag22)
    # bkmark23.save()
    # bkmark24.list_of_tags.add(tag21, tag22)
    # bkmark24.save()

    # reminder1 = models.Reminder(name="reminder1", creator=user1, bookmark=bkmark14, reminder_time=timezone.now()+datetime.timedelta(days=10), time_of_creation=timezone.now())
    # reminder1.save()
    # reminder2 = models.Reminder(name="reminder2", creator=user2, bookmark=bkmark24, reminder_time=timezone.now()+datetime.timedelta(days=20), time_of_creation=timezone.now())
    # reminder2.save()