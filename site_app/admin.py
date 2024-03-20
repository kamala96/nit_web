from django.contrib import admin

from site_app.models import AccountingOfficer, Department, Download, Event, Gallery, Menu, MenuImage, MenuItem, MenuItemContent, OrganizationUnit, Post, Program, QuickLink, Slider, Staff

# Register your models here.


@admin.register(MenuImage)
class MenuImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'menu')

    # @admin.display(description='Associated Menu')
    # def menu_list(self, obj):
    #     return ", ".join([menu.title for menu in obj.menu_images.all()])


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'url', 'order', 'parent_menu',
                    'menu_type', 'page_type', 'is_visible', 'get_joined_images', 'created_at', 'updated_at']
    list_per_page = 50
    list_filter = ['menu_type', 'page_type', 'is_visible']
    search_fields = ['title', 'slug',]
    prepopulated_fields = {'slug': ('title',)}

    def get_joined_images(self, obj):
        if obj.menu_images.exists():
            return ', '.join([image.image.url for image in obj.menu_images.all()])
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
    list_display = ['short_title', 'post_type', 'short_description',  'file_url',
                    'image_url', 'cover_image', 'user', 'created_at', 'updated_at']
    list_per_page = 10
    list_filter = ['post_type']
    search_fields = ['title',]

    @admin.display(description='Title')
    def short_title(self, obj):
        # Truncate description to two lines
        max_length = 60  # Adjust as needed
        if len(obj.description) > max_length:
            return obj.description[:max_length] + '...'
        return obj.description

    @admin.display(description='Description')
    def short_description(self, obj):
        # Truncate description to two lines
        max_length = 60  # Adjust as needed
        if len(obj.description) > max_length:
            return obj.description[:max_length] + '...'
        return obj.description


@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'title', 'order', 'group',
                    'description', 'created_at', 'updated_at']
    list_per_page = 10
    search_fields = ['title',]
    list_filter = ['group',]


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
    list_display = ['full_name', 'title', 'short_welcome_note',
                    'image', 'created_at', 'updated_at']
    list_per_page = 10
    search_fields = ['full_name',]

    @admin.display(description='Welcome Note')
    def short_welcome_note(self, obj):
        # Truncate description to two lines
        max_length = 60
        if len(obj.welcome_note) > max_length:
            return obj.welcome_note[:max_length] + '...'
        return obj.welcome_note


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1


@admin.register(OrganizationUnit)
class OrganizationUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'slug',
                    'unit_type', 'about_note_text', 'get_joined_gallery']
    list_per_page = 10
    search_fields = ['name', 'short_name']
    list_filter = ['unit_type']
    inlines = [DepartmentInline, GalleryInline]

    @admin.display(description='Gallery')
    def get_joined_gallery(self, obj):
        if obj.unit_images.exists():
            return ', '.join([image.image.url for image in obj.unit_images.all()])
        else:
            return 'No images'

    @admin.display(description='About Note')
    def about_note_text(self, obj):
        # Truncate description to two lines
        max_length = 60  # Adjust as needed
        if len(obj.about_note) > max_length:
            return obj.about_note[:max_length] + '...'
        return obj.about_note


class StaffInline(admin.TabularInline):
    model = Staff
    extra = 1


class ProgramInline(admin.TabularInline):
    model = Program
    extra = 1


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'slug', 'unit',
                    'is_academic', 'about_note_text', 'get_joined_gallery']
    list_per_page = 10
    search_fields = ['name', 'short_name', 'slug']
    list_filter = ['unit', 'is_academic']
    readonly_fields = ('created_at', 'updated_at')
    inlines = [StaffInline]

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        if obj and obj.is_academic:
            inline_instances.append(ProgramInline(self.model, self.admin_site))
        return inline_instances

    @admin.display(description='About Note')
    def about_note_text(self, obj):
        # Truncate description to two lines
        max_length = 60  # Adjust as needed
        if len(obj.about_note) > max_length:
            return obj.about_note[:max_length] + '...'
        return obj.about_note

    @admin.display(description='Gallery')
    def get_joined_gallery(self, obj):
        if obj.department_images.exists():
            return ', '.join([image.image.url for image in obj.department_images.all()])
        else:
            return 'No images'


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'department', 'get_short_specialization',
                    'profile_picture', 'is_unit_head', 'is_department_head', 'leadership_title', 'staff_phone', 'staff_email']
    list_per_page = 10
    search_fields = ['name', 'designation',]
    list_filter = ['is_unit_head', 'is_department_head', 'designation']
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Specializaion')
    def get_short_specialization(self, obj):
        # Truncate specialization to two liness
        max_length = 60  # Adjust as needed
        if len(obj.specialization) > max_length:
            return obj.specialization[:max_length] + '...'
        return obj.specialization


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'department',
                    'time_frame', 'is_semester_based', 'get_short_description']
    list_per_page = 10
    search_fields = ['name', 'short_name',]
    list_filter = ['department', 'is_semester_based']
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Description')
    def get_short_description(self, obj):
        # Truncate specialization to two liness
        max_length = 60  # Adjust as needed
        if len(obj.description) > max_length:
            return obj.description[:max_length] + '...'
        return obj.description
