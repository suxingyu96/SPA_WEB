# Generated by Django 4.1.7 on 2023-04-24 08:02

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_student_preference_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='preference_list',
            field=django_mysql.models.ListCharField(models.CharField(max_length=10), max_length=55, size=5),
        ),
    ]
