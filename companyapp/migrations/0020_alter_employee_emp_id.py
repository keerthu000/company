# Generated by Django 4.1.7 on 2024-09-07 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companyapp', '0019_manger_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
