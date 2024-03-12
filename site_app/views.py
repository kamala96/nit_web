from django.shortcuts import render

from site_app.models import Menu

# Create your views here.


def index(request):
    top_menus = Menu.objects.filter(parent_menu__isnull=True)
    context = {
        'menus': top_menus,
    }
    return render(request, 'index.html', context)
