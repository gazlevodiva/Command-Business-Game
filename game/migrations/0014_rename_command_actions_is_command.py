# Generated by Django 4.0.3 on 2022-12-13 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_rename_personalbusinesspayments_businesspayments_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actions',
            old_name='command',
            new_name='is_command',
        ),
    ]
