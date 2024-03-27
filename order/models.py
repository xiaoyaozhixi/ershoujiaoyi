from django.db import models
from user.models import UserInfo
from shop.models import ShopInfo
# Create your models here.
ORDER_STATUS = (
    (0, '未支付'),
    (1, '已支付'),
    (2, '待发货'),
    (3, '待收货'),
    (4, '完成'),
    (5, '拒收'),
)


# 订单表
class PayOrder(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.CharField(unique=True, max_length=32, verbose_name='订单编号')
    order_date = models.DateField(auto_now=True, verbose_name='订单日期')
    order_status = models.IntegerField(choices=ORDER_STATUS, verbose_name='订单状态')
    order_total = models.FloatField(verbose_name='订单总价')
    order_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='订单用户')


ORDERINFO_STATUS = (
    (0, '未支付'),
    (1, '已支付'),
    (2, '已发货'),
    (3, '已完成'),
    (4, '拒绝发货')
)


class OrderInfo(models.Model):
    order_id = models.ForeignKey(PayOrder, on_delete=models.CASCADE, verbose_name='订单表外键', default='')
    buyer = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='买家', related_name='buyer')
    goods = models.ForeignKey(ShopInfo, on_delete=models.CASCADE, verbose_name='商品表')
    goods_count = models.IntegerField(default=1, verbose_name='商品数量')
    goods_total_price = models.FloatField(verbose_name='商品小计')
    goods_price = models.FloatField(verbose_name='商品单价')
    store_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='卖家id', related_name='store_id')
    status = models.IntegerField(choices=ORDERINFO_STATUS, default=0, verbose_name='订单状态')


class CartInfo(models.Model):
    buyer = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='买家')
    goods = models.ForeignKey(ShopInfo, on_delete=models.CASCADE, verbose_name='商品')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number = models.IntegerField(default=1, verbose_name='商品数量')

    def __str__(self):
        return f"{self.buyer.username}'s cart"

