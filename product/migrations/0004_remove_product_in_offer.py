# Generated by Django 3.0.7 on 2020-07-03 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20200704_0024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='in_offer',
        ),
    ]
