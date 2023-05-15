# Generated by Django 4.1.3 on 2023-05-10 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0040_alter_commandpayments_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actions',
            name='category',
            field=models.CharField(choices=[('SLR', 'salary'), ('CMND', 'command'), ('BSNS', 'business'), ('BUY_BSNS', 'buy_business'), ('SELL_BSNS', 'sell_business'), ('DEF_BSNS', 'sell_business'), ('SURP', 'surprise'), ('INFL', 'inflation'), ('NLWL', 'new_level'), ('OTHER', 'other')], default='OTHER', max_length=9),
        ),
        migrations.AlterField(
            model_name='commandpayments',
            name='category',
            field=models.CharField(choices=[('SURP', 'command_surprise'), ('SELL_BIS', 'sell_business'), ('DEPOSITE', 'new_deposite'), ('WITHDRAW', 'withdraw_deposite'), ('BUY_BIS', 'buy_business'), ('OTHER', 'other')], default='OTHER', max_length=8),
        ),
    ]
