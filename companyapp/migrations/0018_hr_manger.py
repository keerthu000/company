# Generated by Django 4.1.7 on 2024-09-06 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companyapp', '0017_company_is_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hr_manger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_hr_manager', models.BooleanField(default=False)),
                ('hr_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(default=None, max_length=254, unique=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companyapp.company')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
