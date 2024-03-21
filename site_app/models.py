import os
from uuid import uuid4
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from phonenumber_field.modelfields import PhoneNumberField

from site_app.validators import validate_image_dimensions, validate_pdf_file

# Create your models here.


def generate_unique_filename(instance, filename, folder):
    """Generate a unique filename for the uploaded file."""
    ext = filename.split('.')[-1]  # Get the file extension
    new_filename = f"{uuid4().hex}.{ext}"  # Generate a random filename
    # Return the new filename with the appropriate path
    return os.path.join(folder, new_filename)


def custom_slider_image_upload_to(instance, filename):
    return generate_unique_filename(instance, filename, 'uploads/slider_images/')


def custom_cover_image_upload_to(instance, filename):
    return generate_unique_filename(instance, filename, 'uploads/images/covers/')


def images_general_upload_to(instance, filename):
    return generate_unique_filename(instance, filename, 'uploads/images/')


def files_general_upload_to(instance, filename):
    return generate_unique_filename(instance, filename, 'uploads/files/')


def files_accounting_officer_upload_to(instance, filename):
    return generate_unique_filename(instance, filename, 'uploads/accounting_officers/')


def menu_images_upload_to(instance, filename):
    return generate_unique_filename(instance, filename, 'uploads/menu_images/')


def gallery_upload_to(instance, filename):
    return generate_unique_filename(instance, filename, 'uploads/gallery/')


def profile_pictures_upload_to(instance, filename):
    return generate_unique_filename(instance, filename, 'uploads/profile_pictures_upload_to/')


def downloads_upload_to(instance, filename):
    return generate_unique_filename(instance, filename, 'uploads/downloads/')


class MenuImage(models.Model):
    image = models.ImageField(upload_to=menu_images_upload_to)
    description = models.TextField(blank=True)
    menu = models.ForeignKey(
        'Menu', related_name="menu_images", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.image.name


class Gallery(models.Model):
    name = models.ImageField(upload_to=gallery_upload_to)
    description = models.TextField(blank=True)
    organization_unit = models.ForeignKey(
        'OrganizationUnit', related_name='unit_images', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(
        'Department', related_name='department_images', on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        super().clean()

        if self.organization_unit and self.department:
            raise ValidationError(
                "Either organization_unit or department can have a value, but not both.")
        elif not self.organization_unit and not self.department:
            raise ValidationError(
                "Either organization_unit or department must have a value.")

    def __str__(self):
        return self.name


class Menu(models.Model):
    menu_type_choices = [
        ('A', 'Link'),
        ('B', 'Single Column Child'),
        ('C', 'Multi Column Child')
    ]
    PAGE_TYPE_CHOICES = [
        ('A', 'FACULTIES/DIRECTORATES'),
        ('B', 'DEPARTMENTS/UNITS/CENTERS'),
        ('C', 'OTHER')
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    url = models.CharField(max_length=255)
    order = models.DecimalField(max_digits=20, decimal_places=4)
    parent_menu = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='submenus')
    menu_type = models.CharField(max_length=1, choices=menu_type_choices)
    page_type = models.CharField(
        max_length=1, choices=PAGE_TYPE_CHOICES, default="C")
    is_visible = models.BooleanField(
        default=False, help_text='Whether a menu is visible or not (draft)')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order',]

    def __str__(self):
        return self.title

    def has_children(self):
        return self.submenus.exists()


class MenuItem(models.Model):
    heading = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    is_visible = models.BooleanField(
        default=False, help_text='Whether a menu item is visible or not (draft)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        ordering = ['heading', 'name',]

    def __str__(self):
        return self.name


class MenuItemContent(models.Model):
    menu_item = models.OneToOneField(MenuItem, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Menu Item Content"
        verbose_name_plural = "Menu Items Content"
        ordering = ['menu_item', 'created_at',]

    def __str__(self):
        return f"Content for {self.menu_item.name}"


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(
        max_length=200, verbose_name="Address/Location/Venue")
    image_url = models.ImageField(upload_to='uploads/events/', null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.BooleanField(
        default=False, help_text='Whether it is publishable or not (draft)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title.upper()


class Post(models.Model):
    post_type_choices = [
        ('A', 'Announcements'),
        ('B', 'Latest News'),
        ('C', 'Current News'),
        ('D', 'e-News Flash')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post_type = models.CharField(max_length=1, choices=post_type_choices)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    file_url = models.FileField(
        upload_to=files_general_upload_to, max_length=255, verbose_name='File', null=True, blank=True)

    image_url = models.ImageField(
        upload_to=images_general_upload_to, max_length=255, verbose_name='Image', null=True, blank=True)
    cover_image = models.ImageField(
        upload_to=custom_cover_image_upload_to, verbose_name='Cover Image', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.post_type == 'A':
            if not self.file_url:
                raise ValidationError("For Announcements, file is required.")
            if self.image_url:
                raise ValidationError(
                    "For Announcements, image is not required.")
        if self.post_type == 'B' and not self.image_url:
            if self.file_url:
                raise ValidationError("For Latest News, file is not required.")
            if not self.image_url:
                raise ValidationError("For Latest News, image is required.")
        elif self.post_type == 'C' and (self.image_url or self.file_url or self.cover_image):
            raise ValidationError(
                "For Announcements and Hot News, the image and file are not required.")
        elif self.post_type == 'D' and not (self.image_url and self.file_url):
            raise ValidationError(
                "For e-News Flash, both image and file are required.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run full validation
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title.upper()


class QuickLink(models.Model):
    GROUP_CHOICES = (
        ('A', 'Group A'),
        ('B', 'Group B'),
    )

    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(null=True, blank=True)
    group = models.CharField(max_length=20, choices=GROUP_CHOICES)
    order = models.PositiveIntegerField(help_text="Arrangement in number")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order',]
        unique_together = ['order', 'group',]
        verbose_name = 'Quick Link'
        verbose_name_plural = 'Quick Links'

    def __str__(self):
        return self.title.upper()


class Download(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='uploads/downloads/',
                            validators=[validate_pdf_file])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def get_file_extension(self):
        _, extension = os.path.splitext(self.file.name)
        return extension.lower()


class Slider(models.Model):
    image = models.ImageField(
        upload_to=custom_slider_image_upload_to, max_length=255)
    caption = models.CharField(max_length=100)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.caption


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        defaults = {
            'full_name': 'Default Accounting Officer Name - Click to Edit',
            'title': 'Default Accounting Officer Title - Click to Edit',
            'welcome_note': 'Default Welcome Not - Click to Edite',
        }
        obj, created = cls.objects.get_or_create(pk=1, defaults=defaults)
        return obj


class AccountingOfficer(SingletonModel):
    full_name = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    welcome_note = models.TextField()
    image = models.ImageField(
        upload_to=files_accounting_officer_upload_to, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Accounting Officer"
        verbose_name_plural = "Accounting Officer"

    def __str__(self):
        return self.full_name + ' - ' + self.title


class OrganizationUnit(models.Model):
    UNIT_TYPE_CHOICES = (
        ('A', 'Academic'),
        ('B', 'Administrative'),
    )

    UNIT_GROUP_CHOICES = (
        ('A', 'Faculty'),
        ('B', 'Directorate'),
    )

    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    slug = models.CharField(
        max_length=20, help_text="To be used internally to link this model with Menu", unique=True)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES)
    unit_group = models.CharField(max_length=20, choices=UNIT_GROUP_CHOICES)
    about_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Faculties + Directorates'
        verbose_name_plural = 'Faculties + Directorates'

    def __str__(self):
        return self.name


class Department(models.Model):
    DEPARTMENT = 'A'
    UNIT = 'B'
    CENTRE = 'C'
    DEPARTMENT_GROUP_CHOICES = (
        (DEPARTMENT, 'Department'),
        (UNIT, 'Unit'),
        (CENTRE, 'Centre'),
    )

    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    slug = models.CharField(
        max_length=20, help_text="To be used internally to link this model with Menu", unique=True)
    unit = models.ForeignKey(
        OrganizationUnit, on_delete=models.CASCADE, related_name='departments', null=True, blank=True)
    department_group = models.CharField(
        max_length=20, choices=DEPARTMENT_GROUP_CHOICES)
    is_academic = models.BooleanField(default=False)
    has_prefix = models.BooleanField(
        default=True, help_text='Whether a Department/Centre/Unit has to be prefixed with words - Department, Centre or Unit')
    about_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.short_name}'


class Staff(models.Model):
    DESIGNATION_CHOICES = (
        ('professor', 'Professor'),
        ('associate-professor', 'Associate Professor'),
        ('senior-lecturer', 'Senior Lecturer'),
        ('lecturer', 'Lecturer'),
        ('assistant-lecturer', 'Assistant Lecturer'),
        ('tutorial-assistant', 'Tutorial Assistant'),
        ('senior-tutor', 'Senior Tutor'),
        ('tutor', 'Tutor'),
        ('tutor-1', 'Tutor I'),
        ('tutor-2', 'Tutor II'),
        ('researcher', 'Researcher'),
        ('ict-officer-1', 'ICT Officer I'),
        ('ict-officer-2', 'ICT Officer II'),
        ('instructor', 'Instructor'),
        ('instructors-facilitator', 'Instructor/Facilitator'),

        ('senior-cabin-crew-instructor', 'Senior Cabin Crew Instructor'),
        ('senior-flight-operations-instructor',
         'Senior Flight Operations Instructor'),
        ('laboratory-technician', 'Laboratory Technician'),

        ('pro', 'Public relations Officer'),
        ('ppro', 'Principal Public relations Officer'),
        ('administrative-staff', 'Administrative Staff'),
        ('other', 'Other'),
    )

    LEADERSHIP_CHOICES = (
        ('dean', 'Dean'),
        ('director', 'Director'),
        ('head', 'Head'),
        ('coordinator', 'Coordinator'),
        ('center-leader', 'Center Leader'),
    )

    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES)
    staff_email = models.EmailField(null=True, blank=True)
    staff_phone = PhoneNumberField(region="TZ", null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True)
    specialization = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to=profile_pictures_upload_to, blank=True, null=True)
    is_unit_head = models.BooleanField(
        default=False, verbose_name="IS DIRECTORATE/FACULTY LEADER")
    is_department_head = models.BooleanField(
        default=False, verbose_name="IS_DEPARMENT/UNIT/CENTER LEADER")
    leadership_title = models.CharField(
        max_length=100, choices=LEADERSHIP_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.is_unit_head and self.is_department_head:
            raise ValidationError(
                "A staff member cannot be both a organization unit head and a department head.")

        if self.is_department_head or self.leadership_title:
            if not self.leadership_title:
                raise ValidationError(
                    "Leadership title cannot be empty if is_department_head or leadership_title is true.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run full validation
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.designation}'


class Program(models.Model):
    PHD = 'phd'
    MASTERS = 'masters'
    POSTGRADUATE_DIPLOMA = 'postgraduate-diploma'
    BACHELOR_DEGREE = "bachelor-degree"
    DIPLOMA = 'diploma'
    SHORT_COURSE = 'short-course'

    PROGRAM_GROUP_CHOICES = [
        (PHD, 'PhD'),
        (MASTERS, 'Masters'),
        (POSTGRADUATE_DIPLOMA, 'Postgraduate Diploma'),
        (BACHELOR_DEGREE, "Bachelor's Degree"),
        (DIPLOMA, 'Diploma'),
        (SHORT_COURSE, 'Short Course'),
    ]

    SHORT = 'short'
    LONG = 'long'
    PROGRAM_TYPE_CHOICES = [
        (SHORT, 'Short Program'),
        (LONG, 'Long Program'),
    ]

    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='programs')
    duration = models.DecimalField(max_digits=5, decimal_places=2,
                                   help_text="Duration in months for Short Program, in years for Long Program")

    program_group = models.CharField(
        max_length=50, choices=PROGRAM_GROUP_CHOICES)
    program_type = models.CharField(
        max_length=50, choices=PROGRAM_TYPE_CHOICES)
    order = models.IntegerField(
        default=0, help_text="Order in which programs should be displayed in its Group.")

    program_specification = models.TextField(blank=True)
    admission_requirements = models.TextField(blank=True)
    learning_outcomes = models.TextField(blank=True)
    assessment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.department.is_academic:
            raise ValidationError(
                "Programs can only be associated with academic departments.")

        if self.program_type == self.SHORT:
            if self.program_group != self.SHORT_COURSE:
                raise ValidationError(
                    "For Short Programs, program group must be 'Short Course'.")
        elif self.program_type == self.LONG:
            if self.program_group == self.SHORT_COURSE:
                raise ValidationError(
                    "For Long Programs, program group cannot be 'Short Course'.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run full validation
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order', 'program_group', 'duration']
        verbose_name_plural = 'Programmes'

    def __str__(self):
        return self.name

    @property
    def formatted_duration(self):
        if self.duration is None:
            return None

        if self.program_type == Program.LONG:
            years = int(self.duration)
            return f"{years} year{'s' if years > 1 else ''}"
        elif self.program_type == Program.SHORT:
            if self.duration >= 30:  # Assuming 30 days for a month
                months = self.duration / 30
                return f"{months} month{'s' if months > 1 else ''}"
            else:
                return f"{self.duration} day{'s' if self.duration > 1 else ''}"


class Module(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    programs = models.ManyToManyField(Program, through='ModuleProgram')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Modules/Courses'

    def __str__(self):
        return self.name


class ModuleProgram(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, help_text="Related module")
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    year = models.IntegerField(
        blank=True, null=True, help_text='Year of Study, if applies')
    semester = models.IntegerField(
        blank=True, null=True, help_text='Semester of Study, if applies')
    order = models.IntegerField(
        default=0, help_text="Order in which module should be displayed.")

    class Meta:
        ordering = ['order', 'program__program_group']
        verbose_name = 'Module Program (Intermediate)'
        verbose_name_plural = 'Module Program (Intermediate)'

    def clean(self):
        if self.program.program_type == Program.SHORT:
            if self.year is not None or self.semester is not None:
                raise ValidationError(
                    "For Short Programs, year and semester should not be provided.")
        elif self.program.program_type == Program.LONG:
            # Convert duration to months and then divide by 12 to get the number of years
            duration_in_years = int(self.program.duration * 12 / 12)
            if self.year is None or self.semester is None:
                raise ValidationError(
                    "For Long Programs, year and semester must be provided.")
            if self.year not in range(1, duration_in_years + 1):
                raise ValidationError(
                    "Year should be within program duration.")
            if self.semester not in [1, 2]:
                raise ValidationError("Semester should be either 1 or 2.")

    def __str__(self):
        return f"{self.module} - {self.program}"
