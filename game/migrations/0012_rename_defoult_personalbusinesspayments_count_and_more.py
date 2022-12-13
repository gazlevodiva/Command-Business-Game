# Generated by Django 4.0.3 on 2022-11-24 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_alter_commandbusinesspayments_player'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personalbusinesspayments',
            old_name='defoult',
            new_name='count',
        ),
        migrations.RenameField(
            model_name='personalbusinesspayments',
            old_name='level',
            new_name='defoult_probability',
        ),
        migrations.RenameField(
            model_name='personalbusinesspayments',
            old_name='sender',
            new_name='player_business',
        ),
        migrations.RenameField(
            model_name='playersbusiness',
            old_name='command',
            new_name='is_command',
        ),
        migrations.RemoveField(
            model_name='personalbusinesspayments',
            name='value',
        ),
        migrations.AddField(
            model_name='personalbusinesspayments',
            name='player_level',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personalbusinesspayments',
            name='rentability',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
