from django.views.generic import CreateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import TicketList
from .forms import TicketForm
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from organization.models import Floor, ServiceType, IncidentType
from django.views.generic import ListView

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
