# Generated by Django 4.2.4 on 2023-08-10 02:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_remove_group_id_alter_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='code',
            field=models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='모임초대코드'),
        ),
    ]