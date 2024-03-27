# Generated by Django 3.2.23 on 2024-03-14 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='password',
            field=models.CharField(max_length=200, verbose_name='用户密码'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='picture',
            field=models.ImageField(upload_to='static/img/head_img/', verbose_name='头像'),
        ),
    ]
