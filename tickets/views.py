from django.views.generic import CreateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import TicketList
from .forms import TicketForm
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from organization.models import Floor, ServiceType, IncidentType, Department
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

class TicketCreateView(LoginRequiredMixin, CreateView):
    form_class = TicketForm
    template_name = 'tickets/create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.engineer = self.request.user
        try:
            form.save()
            return JsonResponse({'status': 'success', 'message': '提交成功！'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def load_floors(request):
    department_id = request.GET.get('department')
    floors = Floor.objects.none()
    if department_id:
        try:
            # 通过Location模型获取关联楼层
            floors = Floor.objects.filter(
                location__department_id=department_id
            ).order_by('id').distinct()
        except Exception as e:
            print(f"Error loading floors: {str(e)}")
    return render(request, 'tickets/floor_options.html', {'floors': floors})

@login_required
def load_incidents(request):
    service_id = request.GET.get('service_type')
    incidents = IncidentType.objects.none()
    if service_id:
        try:
            service = ServiceType.objects.get(id=service_id)
            if '技术故障' in service.name:
                incidents = IncidentType.objects.order_by('id')
        except ServiceType.DoesNotExist:
            pass
    return render(request, 'tickets/incident_options.html', {
        'incidents': incidents,
        'default_selected': True  # 新增默认选中标记
    })

class MyTicketsView(LoginRequiredMixin, ListView):
    template_name = 'tickets/my_tickets.html'
    model = TicketList
    context_object_name = 'tickets'

    def get_queryset(self):
        return TicketList.objects.filter(engineer=self.request.user)


@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(TicketList, id=ticket_id, engineer=request.user)
    if request.method == 'POST':
        # 手动处理表单数据
        department_id = request.POST.get('department')
        floor_id = request.POST.get('floor')
        service_type_id = request.POST.get('service_type')
        incident_type_id = request.POST.get('incident_type')
        issue = request.POST.get('issue')
        solution = request.POST.get('solution')

        # 验证数据
        errors = {}
        if not department_id:
            errors['department'] = '必须选择部门'
        if not floor_id:
            errors['floor'] = '必须选择楼层'
        if not service_type_id:
            errors['service_type'] = '必须选择服务类型'
        if not issue:
            errors['issue'] = '必须填写问题描述'

        # 检查服务类型是否为“技术故障”
        if service_type_id:
            try:
                service_type = ServiceType.objects.get(id=service_type_id)
                if '技术故障' in service_type.name and not incident_type_id:
                    errors['incident_type'] = '必须选择故障类型'
            except ServiceType.DoesNotExist:
                errors['service_type'] = '无效的服务类型'

        if errors:
            # 如果有错误，返回表单并显示错误信息
            context = {
                'ticket': ticket,
                'departments': Department.objects.all(),
                'floors': Floor.objects.filter(location__department_id=department_id) if department_id else Floor.objects.none(),
                'service_types': ServiceType.objects.all(),
                'incident_types': IncidentType.objects.all() if service_type_id and '技术故障' in ServiceType.objects.get(id=service_type_id).name else IncidentType.objects.none(),
                'errors': errors,
                'form_data': {
                    'department': department_id,
                    'floor': floor_id,
                    'service_type': service_type_id,
                    'incident_type': incident_type_id,
                    'issue': issue,
                    'solution': solution,
                }
            }
            return render(request, 'tickets/update_ticket.html', context)
        else:
            # 保存数据
            ticket.department_id = department_id
            ticket.floor_id = floor_id
            ticket.service_type_id = service_type_id
            ticket.incident_type_id = incident_type_id if incident_type_id else None
            ticket.issue = issue
            ticket.solution = solution
            ticket.save()
            messages.success(request, '工单更新成功！')
            return redirect('my_tickets')
    else:
        # 初始化表单数据
        context = {
            'ticket': ticket,
            'departments': Department.objects.all(),
            'floors': Floor.objects.filter(location__department=ticket.department),
            'service_types': ServiceType.objects.all(),
            'incident_types': IncidentType.objects.all() if ticket.service_type and '技术故障' in ticket.service_type.name else IncidentType.objects.none(),
            'form_data': {
                'department': ticket.department_id,
                'floor': ticket.floor_id,
                'service_type': ticket.service_type_id,
                'incident_type': ticket.incident_type_id,
                'issue': ticket.issue,
                'solution': ticket.solution,
            }
        }
        return render(request, 'tickets/update_ticket.html', context)