# Generated by Django 4.1.3 on 2022-11-18 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_player_visible_alter_playersbusiness_command'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actions',
            old_name='value',
            new_name='count',
        ),
    ]
