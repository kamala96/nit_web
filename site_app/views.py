from django.shortcuts import get_object_or_404, redirect, render
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
    menu = get_object_or_404(Menu, slug=menu_slug)

    if menu.slug in ['home']:
        return redirect('index')

    # Get all MenuItem objects for the clicked menu
    menu_items = menu.menu_items.all()

    # Create a dictionary to store MenuItemContent for each MenuItem
    menu_item_contents = {}

    # Iterate through each MenuItem and retrieve its associated MenuItemContent
    # for item in menu_items:
    #     if item.content:
    #         menu_item_contents[item] = item.content

    template_name = ''
    if menu.menu_type == 'A':
        template_name = 'menu_a_template.html'
    elif menu.menu_type == 'B':
        template_name = 'menu_b_template.html'
    elif menu.menu_type == 'C':
        template_name = 'menu_c_template.html'

    context = {
        'menu': menu,
        'menu_items': menu_items,
        'menu_item_contents': menu_item_contents,
    }
    print(context)

    return render(request, f'nav_menus/{template_name}', context)
