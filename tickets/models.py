from django.db import models
from django.utils import timezone
from organization.models import Department, Floor, ServiceType, IncidentType
from users.models import CustomUser
from datetime import datetime

class TicketList(models.Model):
    engineer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='工程师')
    date = models.DateField('日期', default=timezone.now)
    # time = models.DateTimeField('时间')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='部门')
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT, verbose_name='楼层')
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT, verbose_name='服务类别')
    incident_type = models.ForeignKey(IncidentType, on_delete=models.PROTECT,
                                    verbose_name='故障类别', null=True, blank=True)
    issue = models.TextField('问题描述')
    solution = models.TextField('解决方法', blank=True)

    # current_time = datetime.now()
    # timenow = current_time.strftime("%H:%M:%S")
    created_at = models.DateTimeField(auto_now_add=True)
    # created_at = models.DateTimeField(auto_now_add=False)
    

    class Meta:
        verbose_name = '工单记录'
        verbose_name_plural = '工单记录'

    def __str__(self):
        return f"{self.date} {self.engineer.name}的工单"