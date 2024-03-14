from django.shortcuts import get_object_or_404, render
from .models import Download, Event, Menu, Post
from site_app.models import Menu


def index(request):
    top_menus = Menu.objects.filter(parent_menu__isnull=True)
    posts = Post.objects.all()
    events = Event.objects.all()
    downloads = Download.objects.all()

    context = {
        'menus': top_menus,
        'announcements': posts.filter(post_type='A'),
        'events': events,
        'downloads': downloads,
        'news': posts.filter(post_type='B'),
        'quick_links': posts.filter(post_type='C'),
        'news_flash': posts.filter(post_type='D')
   
    }
    return render(request, 'index.html', context)


def handle_nav_menu_click(request, menu_slug):
    menu_item = get_object_or_404(Menu, slug=menu_slug)
    print(menu_item)
