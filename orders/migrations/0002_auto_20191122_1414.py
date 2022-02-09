# Generated by Django 2.0.3 on 2019-11-22 14:14

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_details',
            name='order_id',
        ),
        migrations.AddField(
            model_name='orders',
            name='order',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.DeleteModel(
            name='Order_Details',
        ),
    ]
