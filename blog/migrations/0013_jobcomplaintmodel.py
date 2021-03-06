# Generated by Django 3.0.3 on 2020-11-19 19:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_jobassignmentmodel_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobcomplaintModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(default='1', max_length=100)),
                ('detail', models.CharField(default='1', max_length=100)),
                ('date', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('status', models.CharField(default='1', max_length=100)),
            ],
            options={
                'verbose_name': 'Job Complaint',
                'verbose_name_plural': 'Job Complaints',
            },
        ),
    ]
