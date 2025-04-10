from django.contrib import admin
from .models import (Department,
                     Floor,
                     Location,
                     ServiceType,
                     IncidentType
                     )


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class FloorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)  # 按名称排序


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'floor', 'combined_info')

    def combined_info(self, obj):
        return f"{obj.department.name} @ {obj.floor.name}"  # 显示楼层名称

    combined_info.short_description = '完整位置信息'


class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 20

class IncidentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 20


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Floor, FloorAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(IncidentType, IncidentTypeAdmin)