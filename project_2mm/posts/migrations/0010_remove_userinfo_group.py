# Generated by Django 4.2.4 on 2023-08-10 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_userinfo_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='group',
        ),
    ]
