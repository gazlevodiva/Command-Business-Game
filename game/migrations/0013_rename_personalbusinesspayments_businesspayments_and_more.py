# Generated by Django 4.0.3 on 2022-12-04 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_rename_defoult_personalbusinesspayments_count_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PersonalBusinessPayments',
            new_name='BusinessPayments',
        ),
        migrations.RenameModel(
            old_name='CommandBusinessPayments',
            new_name='CommandPayments',
        ),
    ]
