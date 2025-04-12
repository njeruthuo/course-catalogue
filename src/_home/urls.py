
from django.conf import settings
from django.conf.urls.static import static

from courses import views as courses_views


from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', courses_views.course_list_view),
    path('courses/<int:course_id>/', courses_views.course_detail_view),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/', courses_views.lesson_detail_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
