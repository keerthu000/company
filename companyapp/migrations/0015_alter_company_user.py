# Generated by Django 4.1.7 on 2024-09-06 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companyapp', '0014_company_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companyapp.cutomeruser'),
        ),
    ]
