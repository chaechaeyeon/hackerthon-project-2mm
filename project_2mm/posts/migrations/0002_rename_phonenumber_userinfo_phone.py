# Generated by Django 4.2.4 on 2023-08-07 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='phonenumber',
            new_name='phone',
        ),
    ]
