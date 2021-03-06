# Generated by Django 3.0.7 on 2020-07-03 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(default=None, max_length=10)),
                ('address', models.TextField(blank=True, max_length=300, null=True)),
                ('city', models.CharField(blank=True, default='Noida', max_length=100, null=True)),
                ('state', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('postal_code', models.IntegerField(blank=True, default=None, null=True)),
                ('age', models.IntegerField(default=20, null=True)),
                ('gender', models.CharField(default='Male', max_length=10, null=True)),
                ('country', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('additional_information', models.TextField(blank=True, max_length=1000, null=True)),
                ('image', models.ImageField(blank=True, default=None, upload_to='Accounts')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
