# Generated by Django 5.0.3 on 2024-03-14 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_app', '0020_delete_category_alter_download_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('heading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='site_app.menu')),
            ],
        ),
        migrations.CreateModel(
            name='MenuItemContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('menu_item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='content', to='site_app.menuitem')),
            ],
        ),
    ]