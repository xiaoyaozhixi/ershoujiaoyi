from django.contrib import admin
from shop.models import *
from django.contrib.admin.models import LogEntry
# Register your models here.


class ShopInfoAdmin(admin.ModelAdmin):
    list_per_pag = 15
    list_display = ['id', 'title', 'type', 'picture', 'price', 'num', 'status', 'description', 'owner']
    list_filter = ['title']
    search_fields = ['title']
admin.site.register(ShopInfo, ShopInfoAdmin)


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', '__str__']
    list_display_links = ['action_time']
    list_filter = ['action_time', 'content_type', 'user']
    readonly_fields = ['action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag',
                       'change_message']

