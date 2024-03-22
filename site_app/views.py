from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import AccountingOfficer, Department, Download, Event, Menu, MenuItem, MenuItemContent, OrganizationUnit, Post, Program, QuickLink, Slider, Staff, StaffDepartmentRelationship
from site_app.models import Menu


def index(request):
    posts = Post.objects.all()
    events = Event.objects.filter(status=True).order_by('-created_at')[:6]
    downloads = Download.objects.order_by('-created_at')[:10]
    sliders = Slider.objects.order_by('-created_at')[:5]
    accounting_officer = AccountingOfficer.load()
    quick_links = QuickLink.objects.all()

    context = {
        'sliders': sliders,
        'announcements': posts.filter(post_type='A').order_by('-created_at')[:6],
        'latest_news': posts.filter(post_type='B').order_by('-created_at')[:4],
        'hot_news': posts.filter(post_type='C').order_by('-created_at')[:6],
        'news_flash': posts.filter(post_type='D').order_by('-created_at').first(),
        'accounting_officer': accounting_officer,
        'events': events,
        'downloads': downloads,
        'quick_links_a': quick_links.filter(group='A')[:7],
        'quick_links_b': quick_links.filter(group='B')[:7],

    }
    return render(request, 'index.html', context)


def catch_non_existing_paths(request, exception=None):
    # return HttpResponseNotFound("Page not found")
    return render(request, 'errors/html/error404.html', status=404)


def custom_500_view(request, exception=None):
    return render(request, 'errors/html/error500.html', status=500)


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
    try:
        menu = Menu.objects.get(slug=menu_slug)
    except Menu.DoesNotExist:
        raise Http404("Oops! It looks like this navigation menu is empty. There's no content to display at the moment. Please check back later or navigate elsewhere on the site.")

    if menu.slug in ['home']:
        return redirect('index')

    nav_data = []
    departments_data = []
    staff_members = []
    leader = None
    accounting_officer = None

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

    if menu.slug in ['about-us']:
        template_name = 'about_us.html'

    if menu.slug in ['rector-message']:
        accounting_officer = AccountingOfficer.load()
        template_name = 'rector_message.html'

    elif menu.page_type.upper() == 'A':

        # Faculties/Directorates
        try:
            org_unit = OrganizationUnit.objects.get(slug=menu.slug.lower())
            nav_data = org_unit
            if org_unit:
                departments_data = org_unit.departments.all()
                # Get all staff department relationships where the department is under the organization unit
                staff_members = StaffDepartmentRelationship.objects.filter(
                    department__unit=org_unit)
                leader = staff_members.filter(is_unit_head=True).first()
        except (OrganizationUnit.DoesNotExist):
            raise Http404(
                "Oops! It looks like this navigation menu is empty. There's no content to display at the moment. Please check back later or navigate elsewhere on the site.")
        template_name = 'faculty_detailed.html'
    elif menu.page_type.upper() == 'B':
        # Units/Departments
        return redirect(reverse('view_department', args=[menu_slug]))

    context = {
        'menu': menu,
        'menu_items': menu_items,
        'menu_item_contents': menu_item_contents,
        'nav_data': nav_data,
        'departments_data': departments_data.filter(is_visible=True) if departments_data else None,
        'staff_members': staff_members,
        'leader': leader,
        'accounting_officer': accounting_officer
    }

    return render(request, f'nav_menus/{template_name}', context)


def handle_view_department(request, department_slug):
    leader = None
    programs = []
    staff_members = []
    try:
        department = Department.objects.get(slug=department_slug)
        programs = Program.objects.filter(department=department)
        staff_members = StaffDepartmentRelationship.objects.filter(
            department=department)
        leader = staff_members.filter(is_department_head=True).first()
    except (Department.DoesNotExist):
        raise Http404("Oops! It looks like this navigation menu is empty. There's no content to display at the moment. Please check back later or navigate elsewhere on the site.")
    except Exception:
        pass

    context = {
        'department': department,
        'leader': leader,
        'programs': programs,
        'staff_members': staff_members,
    }
    return render(request, 'nav_menus/department_detailed.html', context)


def handle_view_program(request, program_id):
    try:
        program = Program.objects.get(pk=program_id)
        modules = program.moduleprogram_set.all()
    except (Department.DoesNotExist, Staff.DoesNotExist):
        raise Http404(
            "Oops! It looks like this navigation is empty. There's no content to display at the moment. Please check back later or navigate elsewhere on the site.")
    except Exception:
        pass

    context = {
        'program': program,
        'modules': modules,
    }
    return render(request, 'nav_menus/program_detailed.html', context)


def handle_news_click(request, news_id):
    posts = Post.objects.all()

    news = get_object_or_404(Post, pk=news_id)
    quick_links = QuickLink.objects.all()

    context = {
        'news': news,
        'latest_news': posts.filter(post_type='B').order_by('-created_at')[:4],
        'quick_links_a': quick_links.filter(group='A')[:7],
    }

    return render(request, 'pages/news_details.html', context)


def handle_event_click(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    context = {
        'event': event
    }

    return render(request, 'pages/event_details.html', context)
