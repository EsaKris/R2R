from django.urls import path
from .views import register, homepage, volunteer, AttendeeListView, prayerRequest, search_fields


urlpatterns = [
    path('Register', register, name="register"),
    path("", homepage, name="homepage"),
    path("send_prayer_request", prayerRequest, name="prayerRequest"),
    path('volunteer/<int:pk>', volunteer, name="volunteer"),
    path('AttendeeListView/', AttendeeListView, name="AttendeeListView"),
    path('search/', search_fields, name="search")
]