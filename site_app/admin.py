from django.contrib import admin

from site_app.models import Menu

# Register your models here.


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'url', 'order',
                    'parent_menu', 'created_at', 'updated_at']
    list_per_page = 10
    list_filter = ['parent_menu']
    search_fields = ['title', 'slug',]
