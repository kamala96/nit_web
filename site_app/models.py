import os
from uuid import uuid4
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

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


class Menu(models.Model):
    menu_type_choices = [
        ('A', 'Link'),
        ('B', 'Single Column Child'),
        ('C', 'Multi Column Child')
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    url = models.CharField(max_length=255)
    order = models.DecimalField(max_digits=5, decimal_places=4)
    parent_menu = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='submenus')
    menu_type = models.CharField(max_length=1, choices=menu_type_choices)
    is_visible = models.BooleanField(
        default=False, help_text='Whether a menu is visible or not (draft)')
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
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField(
        default=False, help_text='Whether it is publishable or not (draft)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title.upper()


class Post(models.Model):
    post_type_choices = [
        ('A', 'Announcements'),
        ('B', 'News'),
        ('C', 'Quick Links'),
        ('D', 'News Flash')
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
    web_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

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
