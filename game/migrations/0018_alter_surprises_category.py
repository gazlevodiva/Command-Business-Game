# Generated by Django 4.0.3 on 2022-12-16 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_remove_playersbusiness_category_business_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surprises',
            name='category',
            field=models.CharField(choices=[('PERSONAL', 'personal'), ('COMMAND', 'command'), ('HORECA', 'horeca'), ('REALTY', 'realty'), ('SCIENCE', 'science'), ('IT', 'IT'), ('MEMO', 'memory')], default='PERSONAL', max_length=10),
        ),
    ]
