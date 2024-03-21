from datetime import timedelta
from django import template
from django.utils import timezone
import re

from site_app.icons import FILE_ICONS
from site_app.models import Menu

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
def truncate_chars(value, max_length):
    if len(value) <= max_length:
        return value
    else:
        truncated_value = value[:max_length]
        words = truncated_value.split(' ')
        words.pop()  # Remove the incomplete word at the end
        return ' '.join(words) + '...'


@register.simple_tag
def get_menu_images(slug):
    try:
        menu = Menu.objects.get(slug=slug)
        print(menu.menu_images.all())
        # return menu.images.all()
        return menu
    except Menu.DoesNotExist:
        return None


@register.filter
def subtract_timedelta(value, days):
    return value - timedelta(days=days)
