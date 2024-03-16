from django.contrib import admin

from site_app.models import AccountingOfficer, Download, Event, Menu, MenuImage, MenuItem, MenuItemContent, Post, Slider

# Register your models here.


@admin.register(MenuImage)
class MenuImageAdmin(admin.ModelAdmin):
    list_display = ('image',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'url', 'order', 'parent_menu',
                    'menu_type', 'is_visible', 'get_joined_images', 'created_at', 'updated_at']
    list_per_page = 50
    list_filter = ['parent_menu']
    search_fields = ['title', 'slug',]
    prepopulated_fields = {'slug': ('title',)}

    def get_joined_images(self, obj):
        if obj.images.exists():
            return ', '.join([image.image.url for image in obj.images.all()])
        else:
            return 'No images'

    get_joined_images.short_description = 'Images'


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['heading', 'name', 'is_visible']
    list_filter = ['heading']
    search_fields = ['heading', 'name']
    list_per_page = 50


@admin.register(MenuItemContent)
class MenuItemContentAdmin(admin.ModelAdmin):
    list_display = ['menu_item', 'content']
    list_filter = ['menu_item']
    list_per_page = 50


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'description',  'address',
                    'image_url', 'start_date', 'end_date', 'status', 'created_at', 'updated_at']
    list_per_page = 10
    list_filter = ['title',]
    search_fields = ['title', 'address',]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_type', 'description',  'file_url',
                    'image_url', 'cover_image', 'web_url', 'user', 'created_at', 'updated_at']
    list_per_page = 10
    list_filter = ['title', 'post_type']
    search_fields = ['title',]


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ['title', 'description',
                    'file', 'user', 'created_at', 'updated_at']
    list_per_page = 10
    search_fields = ['title',]


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['caption', 'image', 'link', 'created_at', 'updated_at']
    list_per_page = 10
    search_fields = ['caption',]


@admin.register(AccountingOfficer)
class AccountingOfficerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'title', 'welcome_note',
                    'image', 'created_at', 'updated_at']
    list_per_page = 10
    search_fields = ['full_name',]
