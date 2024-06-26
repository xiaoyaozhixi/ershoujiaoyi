# Generated by Django 3.2.23 on 2024-03-13 13:24

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20, verbose_name='名称')),
                ('type', models.CharField(max_length=20, verbose_name='类型')),
                ('picture', models.ImageField(upload_to='shop/', verbose_name='图片')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格')),
                ('isDelete', models.BooleanField(default=False)),
                ('status', models.IntegerField(default=1, verbose_name='状态')),
                ('description', models.CharField(blank=True, max_length=300, verbose_name='描述')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userinfo')),
            ],
            managers=[
                ('shop', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CltGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('who_clt', models.CharField(max_length=64)),
                ('owner', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('clt_time', models.DateTimeField(auto_now_add=True)),
                ('clt_relation_note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clt_good', to='shop.shopinfo')),
            ],
        ),
    ]
