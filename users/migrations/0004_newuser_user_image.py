# Generated by Django 4.2.5 on 2023-11-02 16:34

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_newuser_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.handle_user_image),
        ),
    ]
