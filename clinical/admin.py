from django.contrib import admin
from .models import PatientDailyEntry, Prescription, MedicineAdministrationLog, CounselingNote, StatutoryFormRecord

admin.site.register(PatientDailyEntry)
admin.site.register(Prescription)
admin.site.register(MedicineAdministrationLog)
admin.site.register(CounselingNote)
admin.site.register(StatutoryFormRecord)