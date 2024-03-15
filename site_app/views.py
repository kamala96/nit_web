from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Download, Event, Menu, MenuItem, MenuItemContent, Post, Slider
from site_app.models import Menu


def index(request):
    posts = Post.objects.all()
    events = Event.objects.all()
    downloads = Download.objects.all()
    sliders = Slider.objects.order_by('-created_at')[:5]

    context = {
        'sliders': sliders,
        'announcements': posts.filter(post_type='A'),
        'events': events,
        'downloads': downloads,
        'news': posts.filter(post_type='B'),
        'quick_links': posts.filter(post_type='C'),
        'news_flash': posts.filter(post_type='D')

    }
    return render(request, 'index.html', context)


def ajax_handler(request, action):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            # Handle GET request
            if action == 'get_sliders':
                # Limit to 5 latest sliders
                sliders = Slider.objects.order_by('-created_at')[:5]
                sliders_data = [{'image': slider.image.url, 'caption': slider.caption,
                                'link': slider.link} for slider in sliders]
                return JsonResponse({'sliders': sliders_data})
            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)
        elif request.method == 'POST':
            # Handle POST request
            # Implement logic based on the action
            pass
        else:
            return JsonResponse({'error': 'Unsupported method'}, status=405)
    else:
        return JsonResponse({'error': 'No service'}, status=405)


def handle_nav_menu_click(request, menu_slug):
    menu = get_object_or_404(Menu, slug=menu_slug)

    if menu.slug in ['home']:
        return redirect('index')

    # Get all MenuItem objects for the clicked menu
    menu_items = MenuItem.objects.filter(heading=menu)

    # Create a dictionary to store MenuItemContent for each MenuItem
    menu_item_contents = {}

    # Iterate through each MenuItem and retrieve its associated MenuItemContent
    for item in menu_items:
        try:
            menu_item_content = MenuItemContent.objects.get(menu_item=item)
            menu_item_contents[item] = menu_item_content
        except MenuItemContent.DoesNotExist:
            pass

    template_name = '_default.html'
    if menu.slug in ['about-nit']:
        template_name = 'about_nit.html'

    context = {
        'menu': menu,
        'menu_items': menu_items,
        'menu_item_contents': menu_item_contents,
    }

    return render(request, f'nav_menus/{template_name}', context)




def handle_news_click(request, news_id):
    news = get_object_or_404(Post, pk=news_id)

    context = {
        'news': news
    }

    return render(request, 'pages/news_details.html', context)

def handle_event_click(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    context = {
        'event': event
    }

    return render(request, 'pages/event_details.html', context)
