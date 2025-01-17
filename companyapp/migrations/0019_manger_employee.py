# Generated by Django 4.1.7 on 2024-09-07 06:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companyapp', '0018_hr_manger'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_manager', models.BooleanField(default=False)),
                ('mngr_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(default=None, max_length=254, unique=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companyapp.company')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_employee', models.BooleanField(default=False)),
                ('emp_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('emp_id', models.CharField(blank=True, max_length=10, unique=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('department', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(default=None, max_length=254, unique=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('role', models.CharField(blank=True, max_length=20, null=True)),
                ('joining_date', models.DateField(blank=True, max_length=20, null=True)),
                ('salary', models.CharField(blank=True, max_length=20, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companyapp.company')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
