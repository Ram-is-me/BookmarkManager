# Generated by Django 3.2 on 2021-04-25 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark_manager_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Actor',
        ),
    ]