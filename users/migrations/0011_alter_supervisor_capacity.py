# Generated by Django 3.2 on 2023-09-05 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_decisionmaker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supervisor',
            name='capacity',
            field=models.IntegerField(),
        ),
    ]