from django import template
from django.utils import timezone

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
