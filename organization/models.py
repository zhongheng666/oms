from django.db import models

class Department(models.Model):
    """部门模型"""
    name = models.CharField('部门名称', max_length=50, unique=True)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'
        ordering = ['id']

    def __str__(self):
        return self.name

class Floor(models.Model):
    """楼层模型（仅名称）"""
    name = models.CharField('楼层名称', max_length=50, unique=True)

    class Meta:
        verbose_name = '楼层'
        verbose_name_plural = '楼层'
        ordering = ['id']  # 按ID排序

    def __str__(self):
        return self.name

class Location(models.Model):
    """地理位置模型（部门+楼层组合）"""
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name='所属部门'
    )
    floor = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
        verbose_name='所在楼层'
    )

    class Meta:
        verbose_name = '地理位置'
        verbose_name_plural = '地理位置'
        unique_together = ('department', 'floor')  # 组合唯一约束
        ordering = ['department', 'floor']  # 默认排序

    def __str__(self):
        return f"{self.department.name} - {self.floor.name}"

class ServiceType(models.Model):
    """服务类别"""
    name = models.CharField('服务类型', max_length=50, unique=True)

    class Meta:
        verbose_name = '服务类别'
        verbose_name_plural = '服务类别'
        ordering = ['id']

    def __str__(self):
        return self.name

class IncidentType(models.Model):
    """故障类别"""
    name = models.CharField('故障类型', max_length=50, unique=True)

    class Meta:
        verbose_name = '故障类别'
        verbose_name_plural = '故障类别'
        ordering = ['name']

    def __str__(self):
        return self.name