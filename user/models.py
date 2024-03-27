from django.db import models
# Create your models here.


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('用户姓名', max_length=30)
    password = models.CharField('用户密码', max_length=200)
    picture = models.ImageField('头像', upload_to='img/head_img')
    sex = models.CharField('性别', max_length=10)
    phone = models.CharField('手机号码', max_length=20)
    address = models.CharField('地址', max_length=20)
