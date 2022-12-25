from django.contrib import admin
from .models import Customer, Campaign, Message


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'code', 'tag', 'time_zone')
    list_display_links = ('id', 'phone',)
    search_fields = ('phone', 'code', 'tag', 'time_zone')


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'code', 'tag', 'start_time', 'end_time')
    list_display_links = ('id', 'text', )
    search_fields = ('text', 'code', 'tag')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'campaign', 'customer', 'status', 'time_sent')
    list_display_links = ('id', 'time_sent')
    list_editable = ('status',)
    search_fields = ('campaign__text', 'customer__phone',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Message, MessageAdmin)
