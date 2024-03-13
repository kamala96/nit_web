from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Menu(models.Model):
    # title = models.CharField(max_length=100)
    # slug = models.CharField(max_length=100)
    # url = models.CharField(max_length=200)
    # order = models.DecimalField(max_digits=5, decimal_places=4)
    # parent_menu = models.ForeignKey(
    #     'self', on_delete=models.CASCADE, null=True, blank=True, related_name='submenus')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.title
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    url = models.CharField(max_length=255)
    order = models.DecimalField(max_digits=5, decimal_places=4)
    parent_menu = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='submenus')
    submenu_head = models.CharField(max_length=200, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.upper()

    class Meta:
        verbose_name_plural = "categories"


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    file_url = models.FileField(
        upload_to='uploads/files/', null=True, blank=True)
    image_url = models.ImageField(
        upload_to='uploads/images/', null=True, blank=True)
    web_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title.upper()
