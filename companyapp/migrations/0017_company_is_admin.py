# Generated by Django 4.1.7 on 2024-09-06 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companyapp', '0016_alter_company_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
