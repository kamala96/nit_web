import os
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from site_app.models import Slider


@receiver(post_save, sender=Slider)
def delete_old_files(sender, instance, **kwargs):
    # Delete old files if more than five sliders exist
    old_sliders = Slider.objects.order_by('-created_at')[5:]
    for old_slider in old_sliders:
        if old_slider.image:
            # Delete the file from the storage
            if os.path.exists(old_slider.image.path):
                os.remove(old_slider.image.path)
            # Delete the Slider object
            old_slider.delete()


@receiver(pre_delete, sender=Slider)
def delete_slider_file(sender, instance, **kwargs):
    # Delete the file when the Slider object is deleted
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)
