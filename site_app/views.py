from django.shortcuts import render
from itertools import groupby
from operator import itemgetter
from .models import Menu
from site_app.models import Menu


def index(request):
    top_menus = Menu.objects.filter(parent_menu__isnull=True)
    chunk_len = 4
    
    menu_data = []
    for top_menu in top_menus:
        submenus = top_menu.submenus.all()
        # Sort by submenu_head, treating None as an empty string
        submenus = sorted(submenus, key=lambda x: x.submenu_head or '')
        submenu_chunks = [list(group) for _, group in groupby(submenus, key=lambda x: x.submenu_head)]
        menu_data.append({'top_menu': top_menu, 'submenu_chunks': submenu_chunks})
    
    context = {
        'menus': menu_data,
    }
    return render(request, 'index.html', context)
