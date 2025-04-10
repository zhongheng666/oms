# report/templatetags/report_filters.py
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='get_item')
def get_item(value, key):
    """
    安全字典取值过滤器（解决模板中{{ dict|get_item:"key" }}问题）
    功能：当value不是字典时返回0，键不存在时返回0
    """
    try:
        return value.get(key, 0)
    except AttributeError:
        return 0

@register.filter(name='sum_values')
def sum_values(value):
    """
    字典值求和过滤器（解决模板中{{ dict|sum_values }}问题）
    功能：当value不是字典时返回0
    """
    try:
        return sum(value.values())
    except AttributeError:
        return 0

@register.filter
@stringfilter
def format_date(value, format_str="%Y年%m月%d日"):
    """
    日期格式化过滤器（解决模板中{{ date|format_date }}问题）
    """
    from django.utils.dateparse import parse_date
    date_obj = parse_date(value)
    return date_obj.strftime(format_str) if date_obj else value

