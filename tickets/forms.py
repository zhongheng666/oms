from django import forms
from django.utils import timezone
from .models import TicketList
from organization.models import Department, Floor, ServiceType, IncidentType
from datetime import datetime


class TicketForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'readonly': 'readonly'
        }),
        initial=timezone.now().date()
    )

    class Meta:
        model = TicketList
        fields = ['department', 'floor', 'service_type', 'incident_type', 'issue', 'solution']
        widgets = {
            'issue': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', }),
            'solution': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # 动态加载部门
        self.fields['department'].queryset = Department.objects.order_by('id')
        if not self.data:  # 初始加载时设置默认值
            self.initial.setdefault('department', Department.objects.first())

        # 动态加载楼层（修复关键逻辑）
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['floor'].queryset = Floor.objects.filter(
                    location__department_id=department_id
                ).order_by('id')
            except (ValueError, TypeError):
                pass
        elif self.initial.get('department'):
            self.fields['floor'].queryset = Floor.objects.filter(
                location__department=self.initial['department']
            ).order_by('id')
            self.initial.setdefault('floor', self.fields['floor'].queryset.first())

        # 动态加载服务类型
        self.fields['service_type'].queryset = ServiceType.objects.order_by('id')
        if not self.data:
            self.initial.setdefault('service_type', ServiceType.objects.first())

        # 动态加载故障类型（修复关键逻辑）
        if 'service_type' in self.data:
            try:
                service_id = int(self.data.get('service_type'))
                service = ServiceType.objects.get(id=service_id)
                if '技术故障' in service.name:
                    self.fields['incident_type'].queryset = IncidentType.objects.order_by('id')
                    if not self.data.get('incident_type'):
                        self.initial.setdefault('incident_type', IncidentType.objects.first())
                else:
                    self.fields['incident_type'].queryset = IncidentType.objects.none()
            except (ValueError, TypeError, ServiceType.DoesNotExist):
                pass
        elif self.initial.get('service_type'):
            service = self.initial['service_type']
            if '技术故障' in service.name:
                self.fields['incident_type'].queryset = IncidentType.objects.order_by('id')
                self.initial.setdefault('incident_type', IncidentType.objects.first())
            else:
                self.fields['incident_type'].queryset = IncidentType.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        service_type = cleaned_data.get('service_type')
        incident_type = cleaned_data.get('incident_type')

        if service_type and '技术故障' in service_type.name:
            if not incident_type:
                self.add_error('incident_type', '必须选择故障类型')
        else:
            cleaned_data['incident_type'] = None

        return cleaned_data