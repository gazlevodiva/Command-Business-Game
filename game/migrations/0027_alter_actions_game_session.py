# Generated by Django 4.1.3 on 2023-04-25 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0026_actions_game_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actions',
            name='game_session',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='game.gamesessions'),
        ),
    ]
