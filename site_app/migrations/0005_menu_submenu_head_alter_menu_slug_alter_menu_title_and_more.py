# Generated by Django 5.0.3 on 2024-03-13 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_app', '0004_alter_menu_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='submenu_head',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='menu',
            name='url',
            field=models.CharField(max_length=255),
        ),
    ]
