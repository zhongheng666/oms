from django import template

register = template.Library()

@register.filter
def get_item(value, key):
    """安全获取字典值，自动处理非字典类型"""
    if isinstance(value, dict):
        return value.get(key, 0)
    return 0

@register.filter
def sum_values(value):
    """安全求和，自动处理非字典类型"""
    if isinstance(value, dict):
        return sum(value.values())
    return 0
