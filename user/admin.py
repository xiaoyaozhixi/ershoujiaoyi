from django.contrib import admin
from user.models import UserInfo
from django.contrib.admin.models import LogEntry
# Register your models here.


class UserInfoAdmin(admin.ModelAdmin):
    list_per_pag = 15
    list_display = ['id', 'username', 'password', 'picture', 'sex', 'phone', 'address']
    list_filter = ['id', 'username']
    search_fields = ['id', 'username']
admin.site.register(UserInfo, UserInfoAdmin)


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', '__str__']
    list_display_links = ['action_time']
    list_filter = ['action_time', 'content_type', 'user']
    readonly_fields = ['action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag',
                       'change_message']

