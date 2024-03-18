import os
from uuid import uuid4
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

    def __str__(self):
        return self.image.name


class Gallery(models.Model):
    name = models.ImageField(upload_to=gallery_upload_to)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    menu_type_choices = [
        ('A', 'Link'),
        ('B', 'Single Column Child'),
        ('C', 'Multi Column Child')
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    url = models.CharField(max_length=255)
    order = models.DecimalField(max_digits=20, decimal_places=4)
    parent_menu = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='submenus')
    menu_type = models.CharField(max_length=1, choices=menu_type_choices)
    is_visible = models.BooleanField(
        default=False, help_text='Whether a menu is visible or not (draft)')
    description = models.TextField(null=True, blank=True)
    images = models.ManyToManyField(
        'MenuImage', related_name='menu_images', null=True, blank=True)
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
        ('C', 'Hot News'),
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
    title = models.CharField(max_length=20)
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

    name = models.CharField(max_length=100)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES)
    about_note = models.TextField(blank=True)
    gallery = models.ManyToManyField(
        'Gallery', related_name='unit_gallery', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    unit = models.ForeignKey(
        OrganizationUnit, on_delete=models.CASCADE, null=True, blank=True)
    gallery = models.ManyToManyField(
        'Gallery', related_name='department_gallery', null=True, blank=True)
    is_academic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    DESIGNATION_CHOICES = (
        ('professor', 'Professor'),
        ('associate-professor', 'Associate Professor'),
        ('assistant-professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('assistant-lecturer', 'Assistant Lecturer'),
        ('tutor', 'Tutor'),
        ('researcher', 'Researcher'),
        ('ict-officer', 'ICT Officer'),
        ('administrative-staff', 'Administrative Staff'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True)
    specialization = models.ManyToManyField(
        'Specialization', blank=True)
    profile_picture = models.ImageField(
        upload_to=profile_pictures_upload_to, blank=True, null=True)
    is_unit_head = models.BooleanField(default=False)
    is_department_head = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.is_unit_head and self.is_department_head:
            raise ValidationError(
                "A staff member cannot be both a organization unit head and a department head.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run full validation
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Program(models.Model):
    TIMEFRAME_CHOICES = (
        ('0.1', '1 Month'),
        ('0.2', '2 Months'),
        ('0.3', '3 Months'),
        ('0.6', '6 Months'),
        ('1', '1 Year'),
        ('2', '2 Years'),
        ('3', '3 Years'),
        ('4', '4 Years'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, related_name='programs')
    time_frame = models.CharField(
        max_length=100, choices=TIMEFRAME_CHOICES, null=True)
    is_semester_based = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.department.is_academic:
            raise ValidationError(
                "Programs can only be associated with academic departments.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run full validation
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Module(models.Model):
    SEMESTER_CHOICES = (
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
        ('3', 'Semester 3'),
        ('4', 'Semester 4'),
        ('5', 'Semester 5'),
        ('6', 'Semester 6'),
        ('7', 'Semester 7'),
        ('8', 'Semester 8'),
    )
    name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(
        help_text="Duration in weeks", null=True, blank=True)
    semester = models.CharField(
        max_length=100, choices=SEMESTER_CHOICES, null=True, blank=True)
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return self.name
