from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.utils import timezone
import datetime

class User(models.Model):
    name = models.CharField(max_length=50)

class Tag(models.Model):
    class Meta:
        unique_together = (('name', 'creator'), )

    name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=CASCADE)
    date_of_creation = models.DateField(max_length=50)

class Group(models.Model):
    class Meta:
        unique_together = (('name', 'creator'), )

    name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=CASCADE)
    date_of_creation = models.DateField(max_length=50)

class Bookmark(models.Model):
    creator = models.ForeignKey(User, on_delete=CASCADE)
    date_of_creation = models.DateField(max_length=50)
    group = models.ForeignKey(Group, on_delete=CASCADE)
    url = models.URLField(max_length=500)
    custom_name = models.CharField(max_length=50)
    custom_note = models.CharField(max_length=200)
    list_of_tags = models.ManyToManyField(Tag, blank=True)

class Reminder(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    bookmark = models.ForeignKey(Bookmark, on_delete=CASCADE)
    creator = models.ForeignKey(User, on_delete=CASCADE)
    time_of_creation = models.DateTimeField(max_length=100)
    reminder_time = models.DateTimeField(max_length=100)
    status = models.CharField(max_length=10, default="green")

    def compute_status(self):
        if timezone.now() > self.reminder_time:
            self.status = "red"
        elif self.reminder_time - timezone.now() < datetime.timedelta(days=1):
            self.status = "yellow"
        else:
            self.status = "green"

