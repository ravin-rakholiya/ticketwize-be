# Generated by Django 4.2.2 on 2023-06-12 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userevent',
            name='event',
        ),
        migrations.RemoveField(
            model_name='userevent',
            name='user',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='UserEvent',
        ),
    ]
