# Generated by Django 4.0.3 on 2022-12-16 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0019_actions_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playersbusiness',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'personal'), ('SOLD', 'command'), ('DEFOULT', 'horeca')], default='ACTIVE', max_length=10),
        ),
    ]
