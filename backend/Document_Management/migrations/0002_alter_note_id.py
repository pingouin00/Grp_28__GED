# Generated by Django 5.1.7 on 2025-03-30 12:59

import django_mongodb_backend.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Document_Management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='id',
            field=django_mongodb_backend.fields.ObjectIdField(primary_key=True, serialize=False),
        ),
    ]
