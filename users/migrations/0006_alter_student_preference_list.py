# Generated by Django 4.1.7 on 2023-04-23 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_student_preference_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='preference_list',
            field=models.CharField(default='', max_length=100),
        ),
    ]
