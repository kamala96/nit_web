import os
from django.db.models.signals import pre_delete, post_save, post_delete, pre_save
from django.dispatch import receiver
from PIL import Image

from nit_web import settings
from site_app.models import Post, Slider


@receiver(post_save, sender=Post)
def resize_image(sender, instance, **kwargs):
    if instance.post_type == 'D' and instance.image_url:
        accepted_width = settings.NEWS_FLASH_IMAGE_WIDTH
        accepted_height = settings.NEWS_FLASH_IMAGE_HEIGHT
        img = Image.open(instance.image_url.path)
        if img.width != accepted_width or img.height != accepted_height:
            # img = img.resize((accepted_width, accepted_height))
            img = img.resize((accepted_width, accepted_height))
            img.save(instance.image_url.path)


@receiver(post_save, sender=Post)
def resize_and_save_cover_image(sender, instance, created, **kwargs):
    if instance.post_type == 'B' and instance.image_url:
        accepted_cover_width = settings.LATEST_NEWS_COVER_IMAGE_WIDTH
        accepted_cover_height = settings.LATEST_NEWS_COVER_IMAGE_HEIGHT
        img = Image.open(instance.image_url.path)
        img.resize((accepted_cover_width, accepted_cover_height))
        cover_image_directory = os.path.join(
            settings.MEDIA_ROOT, 'uploads/images/covers/')
        os.makedirs(cover_image_directory, exist_ok=True)
        cover_image_path = os.path.join(
            cover_image_directory, instance.image_url.name.split("/")[-1])
        img = img.save(cover_image_path)

        # Save the cover image path only if it's a new instance or cover image is not set
        if created or not instance.cover_image:
            instance.cover_image = cover_image_path
            instance.save(update_fields=['cover_image'])
        else:
            # For existing instances, remove the old cover image file and update the cover_image field
            old_cover_image_path = instance.cover_image
            instance.cover_image = cover_image_path
            Post.objects.filter(pk=instance.pk).update(
                cover_image=instance.cover_image)
            # Delete the old cover image file from the filesystem
            if os.path.exists(old_cover_image_path.path):
                os.remove(old_cover_image_path.path)


@receiver(post_save, sender=Slider)
def resize_slider_image(sender, instance, created, **kwargs):
    if instance.image:  # Check if image exists
        # Get the accepted dimensions from settings
        accepted_width = settings.REQUIRED_SLIDER_IMAGE_WIDTH
        accepted_height = settings.REQUIRED_SLIDER_IMAGE_HEIGHT
        # Open the uploaded image
        img = Image.open(instance.image.path)
        # Check if the image dimensions match the accepted dimensions
        if img.width != accepted_width or img.height != accepted_height:
            # Resize the image to the accepted dimensions
            img = img.resize((accepted_width, accepted_height))
            # Save the resized image back to the original file path
            img.save(instance.image.path)


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
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(post_delete, sender=Post)
def delete_post_file_image(sender, instance, **kwargs):
    # Delete the file and image when the any Post object is deleted
    if instance.file_url:
        if os.path.isfile(instance.file_url.path):
            os.remove(instance.file_url.path)
    if instance.image_url:
        if os.path.isfile(instance.image_url.path):
            os.remove(instance.image_url.path)
    if instance.cover_image:
        if os.path.isfile(instance.cover_image.path):
            os.remove(instance.cover_image.path)


# @receiver(.pre_save, sender=MediaFile)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False

#     try:
#         old_file = MediaFile.objects.get(pk=instance.pk).file
#     except MediaFile.DoesNotExist:
#         return False

#     new_file = instance.file
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
