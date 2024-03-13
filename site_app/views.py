from django.shortcuts import render
from site_app.models import Menu

#new

from itertools import groupby
from operator import itemgetter

# Create your views here.
# def index(request):
#     top_menus = Menu.objects.filter(parent_menu__isnull=True)
    
#     # Fetch submenus for each top-level menu item
#     menus_with_submenus = []
#     for top_menu in top_menus:
#         submenus = Menu.objects.filter(parent_menu=top_menu)
#         menus_with_submenus.append({'top_menu': top_menu, 'submenus': submenus})
    
#     context = {
#         'menus': menus_with_submenus,
#     }
#     return render(request, 'index.html', context)



# def index(request):
#     top_menus = Menu.objects.filter(parent_menu__isnull=True)
#     chunk_len = 4
    
#     menu_data = []
#     for top_menu in top_menus:
#         submenus = top_menu.submenus.all()
#         submenu_chunks = [submenus[i:i+chunk_len] for i in range(0, len(submenus), chunk_len)]
#         menu_data.append({'top_menu': top_menu, 'submenu_chunks': submenu_chunks})
    
#     context = {
#         'menus': menu_data,
#     }
#     return render(request, 'index.html', context)






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


