# Generated by Django 4.2.5 on 2023-10-03 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_newuser_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]