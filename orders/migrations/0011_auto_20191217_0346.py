# Generated by Django 2.0.3 on 2019-12-17 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20191217_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='username',
            field=models.CharField(default=None, max_length=64),
        ),
    ]
