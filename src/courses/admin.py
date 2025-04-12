import helpers
from cloudinary import CloudinaryImage

from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Course, Lesson


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0
    readonly_fields = ['order', 'public_id', 'display_image', 'display_video']

    def display_image(self, obj, *args, **kwargs):
        url = helpers.get_cloudinary_image_object(
            obj, field_name='thumbnail', width=200)
        return format_html(f"<img src={url} />")
    display_image.short_description = "Currrent Image"

    def display_video(self, obj, *args, **kwargs):
        embed_video_html = helpers.get_cloudinary_video_object(
            obj,
            field_name='video',
            as_html=True,
            width=550
        )
        return embed_video_html

    display_video.short_description = "Currrent Video"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title',  'status',  'access']
    list_filter = ['status', 'access']
    fields = ['title', 'public_id', 'description', 'status',
              'image', 'access', "display_image"]

    readonly_fields = ['display_image', 'public_id']
    inlines = [LessonInline]

    def display_image(self, obj, *args, **kwargs):
        url = obj.image_admin
        return format_html(f"<img src={url} />")

    display_image.short_description = "Currrent Image"
