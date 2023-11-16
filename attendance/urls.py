from django.urls import path
from . import views

urlpatterns = [
    path('', views.createAttendance, name='attendance-list'),
    path('attendance-detail/<int:pk>/', views.attendanceDetail, name="attendanceDetail"),
    path('generate_word_doc/<int:pk>/', views.generate_word_doc, name="generate_word_doc"),
]