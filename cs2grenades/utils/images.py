from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def validate_img_size_for_view(image, size=1):
    max_size = size * 1024 * 1024
    if hasattr(image, 'size'):
        return image.size <= max_size
    else:
        return False


def validate_image_size(image, size=1):
    """
    Check the size of image, you can change param SIZE by default it is 1MB
    """
    max_size = size * 1024 * 1024

    if image.file.size > max_size:
        # return False
        raise ValidationError(f'Image is too large, max size is {size}MB')


def validate_image_dimensions(image, width=1920, height=1080):
    """
    Check the dimensions of image, you can change params WIDTH and HEIGHT by default it is \n
    width=1920, height=1080
    """
    try:
        with Image.open(image) as image_opened:
            if image_opened.width > width or image_opened.height > height:
                raise ValidationError(
                    f'Image is too big. Max width is {width} and max height is {height}.'
                )

    except Exception as e:
        raise ValidationError(f'Error processing image: {str(e)}')


def resize_image(image, width, height):
    img = Image.open(image)
    img.thumbnail((width, height), Image.Resampling.LANCZOS)

    img_io = BytesIO()

    if image.name.lower().endswith('.png'):
        format = 'PNG'
    else:
        format = 'JPEG'

    img.save(img_io, format=format)
    img_io.seek(0)

    image_resized = InMemoryUploadedFile(
        img_io,
        None,
        image.name,
        f'image/{format.lower()}',
        img_io.getbuffer().nbytes,
        None
    )

    return image_resized


def image_changed():
    return
