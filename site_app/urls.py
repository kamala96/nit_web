from django.urls import include, path, re_path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/<str:menu_slug>/', views.handle_nav_menu_click,
         name='handle_nav_menu_click'),
    path('ajax/<str:action>/', views.ajax_handler, name='ajax_handler'),

    # robots.txt path below
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
]
