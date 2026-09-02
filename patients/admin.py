from django.contrib import admin
from .models import Patient, PatientTimelineEvent


class PatientTimelineEventInline(admin.TabularInline):
    model = PatientTimelineEvent
    extra = 1


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_code', 'full_name', 'institution', 'admission_type', 'status', 'admission_date', 'assigned_doctor')
    list_filter = ('institution', 'status', 'admission_type', 'gender')
    search_fields = ('full_name', 'patient_code', 'phone', 'emergency_contact_phone')
    inlines = [PatientTimelineEventInline]


@admin.register(PatientTimelineEvent)
class PatientTimelineEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'is_visible_to_family', 'created_at')
    list_filter = ('is_visible_to_family',)