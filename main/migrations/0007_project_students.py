# Generated by Django 4.2.4 on 2023-08-17 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_supervisor_capacity'),
        ('main', '0006_alter_projectlist_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='students',
            field=models.ManyToManyField(related_name='projects', through='main.ProjectList', to='users.student'),
        ),
    ]
