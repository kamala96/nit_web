# Generated by Django 5.0.3 on 2024-03-13 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_app', '0006_event_user_alter_post_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.RemoveField(
            model_name='event',
            name='category',
        ),
    ]