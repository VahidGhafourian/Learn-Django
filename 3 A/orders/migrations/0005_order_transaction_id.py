# Generated by Django 4.2.5 on 2023-10-20 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_order_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(default='', max_length=255),
        ),
    ]
