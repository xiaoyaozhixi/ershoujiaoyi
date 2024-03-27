from django.db import models
from user.models import UserInfo
# Create your models here.


class ShopInfo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('名称', max_length=50)
    type = models.CharField('类型', max_length=20)
    picture = models.ImageField('图片', upload_to='img/shop/')
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    num = models.IntegerField(default=1, verbose_name='数量')
    status = models.IntegerField(default=1, verbose_name='状态')
    description = models.CharField('描述', max_length=300, blank=True)
    owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CltGoods(models.Model):
    clt_relation_note = models.ForeignKey(ShopInfo, on_delete=models.CASCADE, related_name='clt_good')
    who_clt = models.CharField(max_length=64)
    owner = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    clt_time = models.DateTimeField(auto_now_add=True)
