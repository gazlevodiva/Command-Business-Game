# Generated by Django 4.1.3 on 2023-05-04 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0032_remove_moves_game_session_alter_moves_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actions',
            name='player',
        ),
    ]
