# Generated by Django 5.0 on 2025-02-12 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='roles',
            new_name='role',
        ),
    ]
