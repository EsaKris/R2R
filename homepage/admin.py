from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportMixin
from django.contrib import admin
from .models import Attendees


class RegisterAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('Full_Name','Email', 'Phone', 'Gender','Local_Assembly', 'Nationality', 'State_of_Residence', 'Local_Government_Area', 'Are_you_a_pastor', 'will_you_be_camping')
    list_filter = ('Full_Name','Gender','Local_Assembly', 'Nationality', 'State_of_Residence', 'Local_Government_Area', 'Are_you_a_pastor', 'will_you_be_camping')
    search_fields =  ('Full_Name','Gender','Local_Assembly', 'Nationality', 'State_of_Residence', 'Local_Government_Area', 'Are_you_a_pastor', 'will_you_be_camping')
admin.site.register(Attendees, RegisterAdmin)