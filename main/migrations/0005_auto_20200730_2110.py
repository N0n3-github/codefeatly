# Generated by Django 3.0.8 on 2020-07-30 16:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_auto_20200729_1704'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Profile',
        ),
    ]
