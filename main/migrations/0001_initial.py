# Generated by Django 4.1.7 on 2023-04-20 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_student_last_login_supervisor_last_login_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('supervisor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='users.supervisor')),
            ],
        ),
    ]