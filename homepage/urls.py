from django.urls import path
from .views import register, homepage


urlpatterns = [
    path('Register', register, name="register"),
    path("", homepage, name="homepage")   
]