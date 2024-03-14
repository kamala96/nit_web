from django.contrib import admin

from site_app.models import Category, Event, Menu, Post

# Register your models here.


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'url', 'order',
                    'parent_menu', 'menu_type', 'created_at', 'updated_at']
    list_per_page = 50
    list_filter = ['parent_menu']
    search_fields = ['title', 'slug',]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'created_at', 'updated_at']
    list_per_page = 10
    list_filter = ['name']
    search_fields = ['name',]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'description',  'address',
                    'image_url', 'start_date', 'end_date', 'status', 'created_at', 'updated_at']
    list_per_page = 10
    list_filter = ['title',]
    search_fields = ['title', 'address',]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'description',
                    'file_url', 'image_url', 'web_url', 'user', 'created_at', 'updated_at']
    list_per_page = 10
    list_filter = ['title', 'category']
    search_fields = ['title',]
