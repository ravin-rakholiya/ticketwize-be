# Generated by Django 3.2.4 on 2023-07-09 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_user_gender'),
        ('payment', '0004_payment_payment_id'),
        ('content', '0004_auto_20230709_0401'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EventTicket',
            new_name='EventTicketContent',
        ),
    ]
