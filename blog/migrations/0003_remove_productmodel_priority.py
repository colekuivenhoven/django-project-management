# Generated by Django 3.0.3 on 2020-11-11 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_employeemodel_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmodel',
            name='priority',
        ),
    ]
