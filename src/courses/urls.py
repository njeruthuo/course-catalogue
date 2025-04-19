

from .views import *
from django.urls import path

urlpatterns = [
    path('', course_list_view),
    path('<slug:course_id>/', course_detail_view),
    path('<slug:course_id>/lessons/<slug:lesson_id>/', lesson_detail_view),
]
