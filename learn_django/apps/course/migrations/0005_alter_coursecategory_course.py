# Generated by Django 5.0.2 on 2024-03-20 12:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_coursecategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecategory',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='course.course'),
        ),
    ]
