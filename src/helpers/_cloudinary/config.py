import cloudinary
from django.conf import settings

CLOUDINARY_CLOUD_NAME = settings.CLOUDINARY_CLOUD_NAME
CLOUDINARY_CLOUD_PUBLIC_KEY = settings.CLOUDINARY_CLOUD_PUBLIC_KEY
CLOUDINARY_CLOUD_API_SECRET = settings.CLOUDINARY_CLOUD_API_SECRET


def cloudinary_init():
    # Configuration
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_CLOUD_PUBLIC_KEY,
        api_secret=CLOUDINARY_CLOUD_API_SECRET,
        secure=True
    )
