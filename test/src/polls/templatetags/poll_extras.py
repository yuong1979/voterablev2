import bleach
from django import template
from django.conf import settings

register = template.Library()


@register.filter("striptags_except", is_safe=True)
def striptags_except(value, args):
    """Any HTML tags not in the args list will be escaped or stripped from the text"""
    arg_list = [arg.strip() for arg in args.split(',')]
    ret = bleach.clean(value, tags=arg_list, strip=True,
                       attributes=settings.BLEACH_ALLOWED_ATTRIBUTES,
                       styles=settings.BLEACH_ALLOWED_STYLES)
    return ret





@register.filter
def counter_for_pagination(value, counter):
    return value + counter


@register.filter
def total_count(page_number, per_page):
    return (page_number-1) * per_page 