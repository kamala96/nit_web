

from .models import Menu


def menu_context(request):
    # Retrieve all menu items
    top_menus = Menu.objects.filter(parent_menu__isnull=True)
    return {'menus': top_menus}
