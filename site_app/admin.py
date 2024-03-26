from django.contrib import admin

from site_app.models import AccountingOfficer, Council, Department, Download, Event, Gallery, ManagementTeam, Menu, MenuImage, MenuItem, MenuItemContent, Module, ModuleProgram, OrganizationUnit, Post, Program, QuickLink, Slider, Staff, StaffDepartmentRelationship, TopManagementTeam
from site_app.utilities import get_short_description

# Register your models here.


class MenuImageInline(admin.TabularInline):
    model = MenuImage
    extra = 1


class ModuleProgramInline(admin.TabularInline):
    model = ModuleProgram
    extra = 1


@admin.register(MenuImage)
class MenuImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'menu')


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1


class StaffDepartmentRelationshipInline(admin.TabularInline):
    model = StaffDepartmentRelationship
    extra = 1


class ProgramInline(admin.TabularInline):
    model = Program
    extra = 1


class CouncilInline(admin.StackedInline):
    model = Council
    can_delete = True  # Set to True if you want to allow deleting inline objects


class ManagementTeamInline(admin.StackedInline):
    model = ManagementTeam
    can_delete = True


class TopManagementTeamInline(admin.StackedInline):
    model = TopManagementTeam
    can_delete = True


class MenuItemContentInline(admin.StackedInline):
    model = MenuItemContent
    can_delete = True


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'url', 'order', 'parent_menu',
                    'menu_type', 'page_type', 'is_visible', 'get_joined_images', 'created_at', 'updated_at']
    list_per_page = 50
    list_filter = ['menu_type', 'page_type', 'is_visible']
    search_fields = ['title', 'slug',]
    prepopulated_fields = {'slug': ('title',)}
    inlines = [MenuImageInline]

    def get_joined_images(self, obj):
        if obj.menu_images.exists():
            return ', '.join([image.image.url for image in obj.menu_images.all()])
        else:
            return 'No images'

    get_joined_images.short_description = 'Images'


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['heading', 'name', 'is_visible', 'order']
    list_filter = ['heading']
    search_fields = ['heading', 'name']
    inlines = [MenuItemContentInline]
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
    readonly_fields = ('created_at', 'updated_at',)

    @admin.display(description='Title')
    def short_title(self, obj):
        return get_short_description(obj, field_name='title')

    @admin.display(description='Description')
    def short_description(self, obj):
        return get_short_description(obj, field_name='description')


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
        return get_short_description(obj, field_name='welcome_note')


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
        return get_short_description(obj, field_name='about_note', max_length=70)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'slug', 'unit', 'department_group', 'is_academic',
                    'has_prefix', 'is_visible', 'about_note_text', 'get_joined_gallery']
    list_per_page = 10
    search_fields = ['name', 'short_name', 'slug']
    list_filter = ['unit', 'is_academic']
    readonly_fields = ('created_at', 'updated_at')
    inlines = [StaffDepartmentRelationshipInline]

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        if obj and obj.is_academic:
            inline_instances.append(ProgramInline(self.model, self.admin_site))
        return inline_instances

    @admin.display(description='About Note')
    def about_note_text(self, obj):
        return get_short_description(obj, field_name='about_note')

    @admin.display(description='Gallery')
    def get_joined_gallery(self, obj):
        if obj.department_images.exists():
            return ', '.join([image.image.url for image in obj.department_images.all()])
        else:
            return 'No images'


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'display_departments', 'get_short_specialization',
                    'profile_picture', 'staff_phone', 'staff_email',]
    list_per_page = 10
    search_fields = ['name', 'designation', 'staff_email', 'staff_phone']
    readonly_fields = ('created_at', 'updated_at')
    inlines = [StaffDepartmentRelationshipInline, CouncilInline,
               ManagementTeamInline, TopManagementTeamInline]

    @admin.display(description='Specializaion')
    def get_short_specialization(self, obj):
        return get_short_description(obj, field_name='specialization')

    @admin.display(description='Departments')
    def display_departments(self, obj):
        # Fetch and format the list of programs (by short_name)
        departments = obj.departments.all()
        if departments:
            return ', '.join(department.name for department in departments)
        else:
            return 'No department associated'


@admin.register(Council)
class CouncilAdmin(admin.ModelAdmin):
    list_display = ['staff', 'manager']
    search_fields = ['staff__name', 'manager__name',]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ManagementTeam)
class ManagementTeamAdmin(admin.ModelAdmin):
    list_display = ['staff', 'manager']
    search_fields = ['staff__name', 'manager__name',]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TopManagementTeam)
class TopManagementTeamAdmin(admin.ModelAdmin):
    list_display = ['staff', 'manager']
    search_fields = ['staff__name', 'manager__name',]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'department_short_name', 'duration', 'program_group', 'program_type', 'order',
                    'get_short_program_specification', 'get_short_admission_requirements', 'get_short_learning_outcomes', 'get_short_assessment']
    search_fields = ['name', 'short_name',]
    list_filter = ['department', 'program_group', 'program_type']
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 10
    inlines = [ModuleProgramInline]

    @admin.display(description='Department')
    def department_short_name(self, obj):
        return obj.department.short_name

    @admin.display(description='Program Specification')
    def get_short_program_specification(self, obj):
        return get_short_description(obj, field_name='program_specification')

    @admin.display(description='Admission Requirements')
    def get_short_admission_requirements(self, obj):
        return get_short_description(obj, field_name='admission_requirements')

    @admin.display(description='Learning Outcomes')
    def get_short_learning_outcomes(self, obj):
        return get_short_description(obj, field_name='learning_outcomes')

    @admin.display(description='Assessment')
    def get_short_assessment(self, obj):
        return get_short_description(obj, field_name='assessment')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'display_programs',]
    search_fields = ['name', 'code',]
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 10

    @admin.display(description='Programs')
    def display_programs(self, obj):
        # Fetch and format the list of programs (by short_name)
        programs = obj.programs.all()
        if programs:
            return ', '.join(program.short_name for program in programs)
        else:
            return 'No programs associated'


@admin.register(ModuleProgram)
class ModuleProgramAdmin(admin.ModelAdmin):
    list_display = ['module_formatted_name',
                    'program_short_name', 'year', 'semester', 'order',]
    list_per_page = 10

    @admin.display(description='Module')
    def module_formatted_name(self, obj):
        return f'{obj.module.name} ({obj.module.code})'

    @admin.display(description='Program')
    def program_short_name(self, obj):
        return obj.program.short_name
