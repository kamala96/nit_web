from django.shortcuts import get_object_or_404, render
from .models import Download, Event, Menu, Post
from site_app.models import Menu


def index(request):
    posts = Post.objects.all()
    events = Event.objects.all()
    downloads = Download.objects.all()

    context = {
        'announcements': posts.filter(post_type='A'),
        'events': events,
        'downloads': downloads,
        'news': posts.filter(post_type='B'),
        'quick_links': posts.filter(post_type='C'),
    }
    return render(request, 'index.html', context)


def handle_nav_menu_click(request, menu_slug):
    menu_item = get_object_or_404(Menu, slug=menu_slug)

    template_name = ''
    if menu_item.menu_type == 'A':
        template_name = 'menu_a_template.html'
    elif menu_item.menu_type == 'B':
        template_name = 'menu_b_template.html'
    elif menu_item.menu_type == 'C':
        template_name = 'menu_c_template.html'

    return render(request, f'nav_menus/{template_name}', {'menu_item': menu_item})
