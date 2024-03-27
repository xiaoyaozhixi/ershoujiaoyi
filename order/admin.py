from django.contrib import admin
from order.models import *
# Register your models here.


class PayOrderAdmin(admin.ModelAdmin):
    list_per_pag = 15
    list_display = ['id', 'order_number', 'order_date', 'order_status', 'order_total', 'order_user']
    list_filter = ['id', 'order_user']
    search_fields = ['id', 'order_user']
admin.site.register(PayOrder, PayOrderAdmin)


class OrderInfoAdmin(admin.ModelAdmin):
    list_per_pag = 15
    list_display = ['order_id', 'buyer', 'goods', 'goods_count', 'goods_total_price', 'goods_price',
                    'store_id', 'status']
    list_filter = ['order_id', 'buyer']
    search_fields = ['order_id', 'buyer']
admin.site.register(OrderInfo, OrderInfoAdmin)


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', '__str__']
    list_display_links = ['action_time']
    list_filter = ['action_time', 'content_type', 'user']
    readonly_fields = ['action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag',
                       'change_message']