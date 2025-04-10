from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib.admin import DateFieldListFilter
from django.utils import timezone
from django.http import Http404
from datetime import date
from collections import defaultdict
from .models import ReportAutoConfig

# 导入你的模型
from tickets.models import TicketList
from organization.models import Department, Location, ServiceType, IncidentType
from users.models import CustomUser
from .models import ReportQuery
from django.conf import settings

def generate_report(request):
    # 处理日期参数
    try:
        query_date = request.GET.get('date', timezone.localdate().isoformat())
        date_obj = date.fromisoformat(query_date)
    except ValueError:
        raise Http404("无效的日期格式")

    # 获取所有基础数据（优化查询）
    departments = Department.objects.prefetch_related(
        'location_set__floor'
    ).order_by('id')

    service_types = ServiceType.objects.all()
    incident_types = IncidentType.objects.all()

    # 获取当天的所有工单（优化查询）
    tickets = TicketList.objects.filter(date=date_obj).select_related(
        'department',
        'floor',
        'service_type',
        'incident_type'
    )

    # 构建工单索引 { (部门ID, 楼层ID): [工单列表] }
    ticket_index = defaultdict(list)
    for ticket in tickets:
        key = (ticket.department_id, ticket.floor_id)
        ticket_index[key].append(ticket)

    # 初始化报表数据结构
    report_data = {
        'total': {
            'services': {st.name: 0 for st in service_types},
            'incidents': {it.name: 0 for it in incident_types}
        },
        'departments': {}
    }

    # 部门级别统计
    for dept in departments:
        dept_data = {
            'total': {
                'services': {st.name: 0 for st in service_types},  # 确保是字典
                'incidents': {it.name: 0 for it in incident_types}
            },
            'floors': {}
        }

        # 获取部门的所有楼层（通过Location）
        locations = dept.location_set.select_related('floor')
        for loc in locations:
            floor = loc.floor
            floor_tickets = ticket_index.get((dept.id, floor.id), [])

            # 初始化楼层数据
            floor_data = {
                'services': {st.name: 0 for st in service_types},  # 确保是字典
                'incidents': {it.name: 0 for it in incident_types}
            }

            # 统计服务类型
            service_counts = defaultdict(int)
            for ticket in floor_tickets:
                service_counts[ticket.service_type.name] += 1
            
            # 统计故障类型
            incident_counts = defaultdict(int)
            for ticket in floor_tickets:
                if ticket.incident_type:
                    incident_counts[ticket.incident_type.name] += 1

            # 填充数据
            for st in service_types:
                count = service_counts.get(st.name, 0)
                floor_data['services'][st.name] = count
                dept_data['total']['services'][st.name] += count
                report_data['total']['services'][st.name] += count

            for it in incident_types:
                count = incident_counts.get(it.name, 0)
                floor_data['incidents'][it.name] = count
                dept_data['total']['incidents'][it.name] += count
                report_data['total']['incidents'][it.name] += count

            dept_data['floors'][floor.name] = floor_data

        report_data['departments'][dept.name] = dept_data

    # 保存查询记录
    if request.user.is_authenticated:
        ReportQuery.objects.create(
            query_date=date_obj,
            created_by=request.user
        )

    return render(request, 'admin/report/result.html', {
        'query_date': date_obj,
        'report_data': report_data,
        'service_types': service_types,
        'incident_types': incident_types,
    })

@admin.register(ReportQuery)
class ReportQueryAdmin(admin.ModelAdmin):
    list_display = ('query_date', 'created_by', 'created_at')
    list_filter = (('query_date', DateFieldListFilter), 'created_by')
    date_hierarchy = 'query_date'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate/', self.admin_site.admin_view(generate_report), 
                 name='report_generate'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        return redirect(reverse('admin:report_generate'))


# 新增代码（不影响原有ReportQueryAdmin）
@admin.register(ReportAutoConfig)
class ReportAutoConfigAdmin(admin.ModelAdmin):
    list_display = ('execute_time', 'save_path', 'is_active')
    actions = ['test_generate']

    def test_generate(self, request, queryset):
        from .auto_generate import ReportGenerator
        ReportGenerator.generate_daily_report('/tmp/')
        self.message_user(request, "测试生成成功")
    test_generate.short_description = "立即测试生成"

