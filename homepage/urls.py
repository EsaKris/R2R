from django.urls import path
from .views import register, homepage, volunteer, AttendeeListView, prayerRequest, search_fields, donate, inhouse, onlinestream


urlpatterns = [
    path('TV', register, name="register"),
    path("", homepage, name="homepage"),
    path("donate", donate, name="donate"),
    path("send_prayer_request", prayerRequest, name="prayerRequest"),
    path('volunteer/<int:pk>', volunteer, name="volunteer"),
    path('AttendeeListView/', AttendeeListView, name="AttendeeListView"),
    path('search/', search_fields, name="search"),
    path('inhouse/', inhouse, name="inhouse"),
    path('stream/', onlinestream, name="stream")
]