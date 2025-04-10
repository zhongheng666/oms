from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', '系统管理员'),
        ('operator', '运维人员'),
    )
    
    name = models.CharField('姓名', max_length=50)
    role = models.CharField('角色', max_length=10, 
                          choices=ROLE_CHOICES, 
                          default='admin')  # 设置默认角色
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username