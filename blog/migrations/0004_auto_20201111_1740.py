# Generated by Django 3.0.3 on 2020-11-11 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_productmodel_priority'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productmodel',
            old_name='title',
            new_name='name',
        ),
    ]
