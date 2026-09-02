from django import forms
from .models import PatientDailyEntry, Prescription, CounselingNote, StatutoryFormRecord


class PatientDailyEntryForm(forms.ModelForm):
    class Meta:
        model = PatientDailyEntry
        fields = [
            'kind',
            'risk_level',
            'mental_condition',
            'physical_condition',
            'mood',
            'withdrawal_symptoms',
            'sleep_quality',
            'appetite',
            'medicines_given',
            'notes',
        ]
        widgets = {
            'withdrawal_symptoms': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            'medicine_name',
            'dosage',
            'frequency',
            'duration',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class CounselingNoteForm(forms.ModelForm):
    class Meta:
        model = CounselingNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter session observations, progress, and therapy notes...'}),
        }


class StatutoryFormRecordForm(forms.ModelForm):
    class Meta:
        model = StatutoryFormRecord
        fields = ['form_type', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter legal justification, guardian consent details, or incident log...'}),
        }