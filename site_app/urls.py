from django.urls import include, path, re_path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/<str:menu_slug>/', views.handle_nav_menu_click,
         name='handle_nav_menu_click'),
    path('department/<str:department_slug>/', views.handle_view_department,
         name='view_department'),
    path('program/<int:program_id>/', views.handle_view_program,
         name='view_program'),
    path('ajax/<str:action>/', views.ajax_handler, name='ajax_handler'),

    path('news/<int:news_id>/', views.handle_news_click,
         name='handle_news_click'),
    path('event/<int:event_id>/', views.handle_event_click,
         name='handle_event_click'),
    path('programmes-offered/', views.programmes_offered,
         name='programmes_offered'),
    path('programmes-offered/<int:menu_id>/', views.programmes_offered,
         name='programmes_offered_2'),

    # robots.txt path below
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
]
