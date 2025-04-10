from django.db import models
from django.conf import settings

class ReportQuery(models.Model):
    """ 报表查询记录 """
    query_date = models.DateField('查询日期')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='创建人'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '报表查询'
        verbose_name_plural = '报表查询'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.query_date} 报表查询"

# 新增代码（不影响原有ReportQuery模型）
class ReportAutoConfig(models.Model):
    """ 新增的自动生成配置 """
    save_path = models.CharField('保存路径', max_length=500, default='/reports/')
    execute_time = models.TimeField('执行时间', default='06:00:00')
    is_active = models.BooleanField('启用自动', default=True)

    class Meta:
        verbose_name = '自动生成配置'
        verbose_name_plural = '自动生成配置'

    def __str__(self):
        return f"每日{self.execute_time}生成"

