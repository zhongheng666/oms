from django.contrib import admin
from .models import TicketList
from django.contrib.admin import DateFieldListFilter
from users.models import CustomUser  # 新增关键导入

@admin.register(TicketList)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'engineer_name',
        'date', 
        'department', 
        'floor', 
        'service_type',
        'incident_type',
        'issue',
        'solution',
        'created_at'
    ]

    list_filter = [
        ('engineer', admin.RelatedOnlyFieldListFilter),
        ('date', DateFieldListFilter),
        'service_type',
        'incident_type',
        'department'
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'engineer',
            'department',
            'floor',
            'service_type',
            'incident_type'
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 修复后的正确查询
        if db_field.name == 'engineer':
            kwargs["queryset"] = CustomUser.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # 添加以下方法显示更友好的字段名称
    def engineer_name(self, obj):
        return obj.engineer.name
    engineer_name.short_description = '工程师姓名'
