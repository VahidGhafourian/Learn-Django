# Generated by Django 4.2.5 on 2023-10-20 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_transaction_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='transaction_id',
        ),
    ]
