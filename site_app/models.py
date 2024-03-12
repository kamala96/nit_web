from django.db import models

# Create your models here.


class Menu(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order = models.DecimalField(max_digits=5, decimal_places=4)
    parent_menu = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='submenus')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
