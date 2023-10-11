from django.urls import path
from .views import register

urlpatterns = [
    path('Register', register, name="register")   
]