# Generated by Django 3.2 on 2021-04-27 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark_manager_app', '0004_auto_20210426_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='status',
            field=models.CharField(default='green', max_length=10),
        ),
    ]
