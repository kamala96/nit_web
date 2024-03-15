from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/<str:menu_slug>/', views.handle_nav_menu_click,
         name='handle_nav_menu_click'),
    path('ajax/<str:action>/', views.ajax_handler, name='ajax_handler'),
]
