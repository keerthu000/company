# Generated by Django 4.1.7 on 2024-09-09 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companyapp', '0035_leaverequest_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaverequest',
            name='requested_on',
        ),
    ]