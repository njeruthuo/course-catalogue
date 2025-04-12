import uuid
import helpers

from django.db import models
from django.utils.text import slugify

from cloudinary.models import CloudinaryField


helpers.cloudinary_init()


class PublishStatus(models.TextChoices):
    PUBLISHED = "pub", "Published"
    DRAFT = 'draft', "Draft"
    COMING_SOON = 'soon', "Coming soon"


class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = 'email', "Email required"


def handle_upload(instance, filename):
    return f"{filename}"


def generate_public_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-", "")
    if not title:
        return unique_id

    slug = slugify(title)
    unique_short_id = unique_id[:5]
    return f"courses/{slug}-{unique_short_id}"


def get_public_id_prefix(instance, *args, **kwargs):
    if hasattr(instance, "path"):
        path = instance.path
        if path.startswith('/'):
            path = path[1:]
        if path.endswith('/'):
            path = path[:1]
        return path

    public_id = instance.public_id

    model_class = instance.__class__
    model_name = model_class.__name__

    model_name_slug = slugify(model_name)

    if not public_id:
        return f"courses/{model_name_slug}"

    return f"{model_name_slug}/{public_id}"


def get_display_name(instance, *args, **kwargs):
    if hasattr(instance, 'get_display_name'):
        return instance.get_display_name()
    elif hasattr(instance, 'title'):
        return instance.title

    model_class = instance.__class__
    model_name = model_class.__name__

    return f"{model_name} Upload"


class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=130, null=True, blank=True)
    # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    image = CloudinaryField(
        'image',
        null=True,
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=['course', 'thumbnails']
    )
    access = models.CharField(
        max_length=20, choices=AccessRequirement.choices, default=AccessRequirement.EMAIL_REQUIRED)
    status = models.CharField(
        max_length=20, choices=PublishStatus.choices, default=PublishStatus.DRAFT)

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED

    def save(self, *args, **kwargs):
        # before save()
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)
        # after save()

    def get_absolute_url(self):
        return self.path

    def get_display_name(self):
        return f"{self.title} - Course"

    @property
    def path(self):
        return f"courses/{self.public_id} - Course"

    @property
    def image_admin(self):
        return helpers.get_cloudinary_image_object(self, field_name='image', as_html=False, width=200)

    def get_image_thumbnail(self, as_html=False, width=500):
        return helpers.get_cloudinary_image_object(self, field_name='image', as_html=as_html, width=width)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    public_id = models.CharField(max_length=130, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)
    thumbnail = CloudinaryField('image',
                                public_id_prefix=get_public_id_prefix,
                                display_name=get_display_name,
                                blank=True,
                                null=True)
    video = CloudinaryField('video', blank=True,
                            public_id_prefix=get_public_id_prefix,
                            display_name=get_display_name, type='private',
                            null=True, resource_type='video')
    can_preview = models.BooleanField(
        default=False, help_text="If the user doesn't have access to this course see this?")
    status = models.CharField(
        max_length=20, choices=PublishStatus.choices, default=PublishStatus.PUBLISHED)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-updated']

    def save(self, *args, **kwargs):
        # before save()
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)
        # after save()

    def get_display_name(self):
        return f"{self.title} - {self.course.get_display_name()}"

    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith('/'):
            course_path = course_path[:-1]

        return f"{course_path}/lessons/{self.public_id}"
