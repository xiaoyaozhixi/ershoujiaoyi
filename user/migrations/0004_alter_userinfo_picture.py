# Generated by Django 3.2.23 on 2024-03-15 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_userinfo_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='picture',
            field=models.ImageField(upload_to='img/head_img', verbose_name='头像'),
        ),
    ]
