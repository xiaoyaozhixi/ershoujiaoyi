from django.http import HttpResponseRedirect
import time
from alipay import AliPay
from django.shortcuts import render, redirect
from django.urls import reverse
from 二手市场.settings import app_private_key_string, alipay_public_key_string
from order.models import *
from shop.models import *
from user.models import *
# Create your views here.


def place_order_more(request):
    data = request.GET
    username = request.session.get('username')
    address = UserInfo.objects.get(username=username).address
    request_data = []
    for key, value in data.items():
        if key.startswith('goods'):
            goods_id = key.split('_')[1]
            count = request.GET.get('count_'+goods_id)
            cart_id = key.split('_')[2]
            request_data.append((int(goods_id), int(count), int(cart_id)))
    if request_data:
        payorder = PayOrder()
        order_number = str(time.time()).replace('.', '')
        payorder.order_number = order_number
        payorder.order_status = 0
        payorder.order_total = 0
        order_total = 0
        total_count = 0
        payorder.order_user = UserInfo.objects.get(username=username)
        payorder.save()
        for goods_id_one, count_one, cart_id in request_data:
            goods = ShopInfo.objects.get(id=goods_id_one)
            orderinfo = OrderInfo()
            orderinfo.order_id = payorder
            orderinfo.buyer = payorder.order_user
            orderinfo.goods = goods
            orderinfo.goods_count = count_one
            orderinfo.goods_price = goods.price
            orderinfo.goods_total_price = goods.price * count_one
            orderinfo.store_id = goods.owner
            goods.num -= count_one
            if goods.num == 0:
                goods.status = 0
            elif goods.num < 0:
                print('商品数量超出')
                return redirect((reverse('user:cart')))
            orderinfo.save()
            order_total += orderinfo.goods_total_price
            total_count += count_one
            cart = CartInfo.objects.get(id=cart_id)
            cart.order_number = order_number
            cart.save()
            goods.save()
        payorder.order_total = order_total
        payorder.save()
    return render(request, 'user/order.html', locals())


def AlipayView(request):
    order_id = request.GET.get('order_id')
    payorder = PayOrder.objects.get(id=order_id)
    # 实例化支付对象
    alipay = AliPay(
        appid='9021000134681993',
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
    )
    # 实例化订单
    order_string = alipay.api_alipay_trade_page_pay(
        subject='二手市场',  # 交易主题
        out_trade_no=payorder.order_number,
        total_amount=str(payorder.order_total),
        return_url='http://127.0.0.1:8000/order/payresult/',
        notify_url='http://127.0.0.1:8000/order/payresult/'
    )
    result = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do?' + order_string
    return HttpResponseRedirect(result)


def payresult(request):
    order_number = request.GET.get('out_trade_no')
    payorder = PayOrder.objects.get(order_number=order_number)
    payorder.order_status = 1
    order_info = payorder.orderinfo_set.all()
    for one in order_info:
        one.status = 1
        one.save()
    payorder.save()
    return render(request, 'user/payresult.html', locals())
