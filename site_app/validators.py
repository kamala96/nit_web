import os
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_pdf_file(value):
    """
    Validator function to ensure that the uploaded file is a PDF.
    """
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    if ext.lower() != '.pdf':
        raise ValidationError('Only PDF files are allowed.')


def validate_image_dimensions(value):
    target_width = settings.REQUIRED_IMAGE_WIDTH  # Target width in pixels
    target_height = settings.REQUIRED_IMAGE_HEIGHT  # Target height in pixels
    width = value.width
    height = value.height
    if width != target_width or height != target_height:
        raise ValidationError("The image dimensions must be exactly {}x{} pixels.".format(
            target_width, target_height))
