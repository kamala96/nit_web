from django.shortcuts import render

from site_app.models import Event, Menu, Post

# Create your views here.


def index(request):
    top_menus = Menu.objects.filter(parent_menu__isnull=True)
    posts = Post.objects.all()
    context = {
        'menus': top_menus,
        'links': posts.filter(category__slug='links'),
        'announcements': posts.filter(category__slug='announcements'),
        'events': Event.objects.all(),
        'news': posts.filter(category__slug='news'),
    }
    return render(request, 'index.html', context)
