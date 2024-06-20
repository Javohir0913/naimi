from django.contrib import admin
from app_service.models import Service


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_name', 'category_id',)
    search_fields = ('service_name',)
    list_filter = ('service_type',)


admin.site.register(Service, ServiceAdmin)
