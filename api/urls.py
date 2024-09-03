from django.urls import path
from . import views
from .views import CourseListView, CourseDetailView


urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('new-courses/', CourseListView.as_view(), name='new-course_list'),
    path('new-courses/<int:pk>/', CourseDetailView.as_view(), name='new-course_detail'),
]
