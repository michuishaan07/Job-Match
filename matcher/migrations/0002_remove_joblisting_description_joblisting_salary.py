# Generated by Django 5.2.4 on 2025-07-05 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joblisting',
            name='description',
        ),
        migrations.AddField(
            model_name='joblisting',
            name='salary',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
