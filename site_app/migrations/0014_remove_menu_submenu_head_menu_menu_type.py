# Generated by Django 5.0.3 on 2024-03-13 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_app', '0013_merge_20240313_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='submenu_head',
        ),
        migrations.AddField(
            model_name='menu',
            name='menu_type',
            field=models.CharField(choices=[('A', 'Link'), ('B', 'Single Column Child'), ('C', 'Multi Column Child')], default='A', max_length=1),
            preserve_default=False,
        ),
    ]
