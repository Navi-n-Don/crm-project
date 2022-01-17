from typing import Any
from django import template

register = template.Library()


@register.simple_tag
def my_url(value: Any, field_name: Any, urlencode: Any = None) -> str:
    """Method for combining requests"""
    url = f"?{field_name}={value}"

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = f"{url}&{encoded_querystring}"

    return url


@register.filter
def replace(value: Any, args: Any) -> str:
    """Template filter for replace string symbols"""
    if len(args.split('|')) != 2:
        return value

    old, new = args.split('|')
    return value.replace(old, new)
