

from django.utils import timezone
from .models import Menu


def menu_context(request):
    # Retrieve all menu items
    top_menus = Menu.objects.filter(parent_menu__isnull=True, is_visible=True)
    return {'menus': top_menus}


def current_datetime(request):
    current_datetime = timezone.localtime(timezone.now())
    return {'now': current_datetime}
