from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportMixin
from django.contrib import admin
from .models import Attendees, Volunteers, prayerRequest


class RegisterAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('Full_Name','Email', 'Phone', 'Gender','Local_Assembly', 'Nationality', 'State_of_Residence', 'Local_Government_Area', 'Are_you_a_pastor', 'will_you_be_camping')
    list_filter = ('Full_Name','Email','Gender','Local_Assembly', 'Nationality', 'State_of_Residence', 'Local_Government_Area', 'Are_you_a_pastor', 'will_you_be_camping')
    search_fields =  ('Full_Name','Email','Gender','Local_Assembly', 'Nationality', 'State_of_Residence', 'Local_Government_Area', 'Are_you_a_pastor', 'will_you_be_camping')
admin.site.register(Attendees, RegisterAdmin)

class VolunteerAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('Attendee', 'Volunteer', 'created')
    list_filter = ('Attendee', 'Volunteer', 'created')
    search_fields = ('Attendee', 'Volunteer', 'created')
admin.site.register(Volunteers, VolunteerAdmin)



class RequestAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('Full_Name', 'Request', 'created')
    list_filter = ('Full_Name', 'Request', 'created')
    search_fields = ('Full_Name', 'Request', 'created')
admin.site.register(prayerRequest, RequestAdmin)
