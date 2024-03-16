from django import template
from django.utils import timezone
import re

from site_app.icons import FILE_ICONS

register = template.Library()


@register.simple_tag
def custom_timesince(value):
    now = timezone.now()
    diff = now - value

    if diff.days >= 365:
        years = diff.days // 365
        return f"{years} yr"
    if diff.days >= 30:
        months = diff.days // 30
        return f"{months} mo"
    if diff.days >= 1:
        return f"{diff.days} d"
    if diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} hr"
    if diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} min"
    return f"{diff.seconds} sec"


@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)


@register.filter
def title_first(value):
    words = value.split()
    if words:
        words[0] = words[0].capitalize()
    return ' '.join(words)


@register.filter
def is_url(value):
    return value.startswith('http://') or value.startswith('https://')


@register.filter
def get_icon_filenames(file_extension):
    """
    Custom template filter to get the icon filenames for a given file extension.
    """
    return FILE_ICONS.get(file_extension.lower())


@register.filter(name='wordcount')
def wordcount(value):
    words = re.findall(r'\w+', value)
    return len(words)


@register.filter
def truncate_with_read_more(value, max_length, read_more_url):
    if len(value) <= max_length:
        return value
    truncated_value = value[:max_length].rsplit(' ', 1)[0] + '...'
    return f'{truncated_value} <a href="{read_more_url}" class="text-blue-500 underline cursor-pointer">Read more</a>'
