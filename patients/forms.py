from django import forms
from .models import Patient, PatientTimelineEvent
from accounts.models import User


class PatientAdmissionForm(forms.ModelForm):
    admission_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Patient
        fields = [
            'admission_type',
            'full_name',
            'age',
            'gender',
            'phone',
            'aadhaar_number',
            'address',
            'admission_date',
            'addiction_type',
            'medical_history',
            'diagnosis',
            'assigned_doctor',
            # Emergency
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relation',
            # Guardian / Minor / Legal
            'guardian_name',
            'guardian_phone',
            'guardian_relation',
            'school_name',
            'grade',
            'legal_reason',
            'legal_remarks',
            # Consents
            'self_consent',
            'digital_signature',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 2}),
            'legal_reason': forms.Textarea(attrs={'rows': 2}),
            'legal_remarks': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        institution = kwargs.pop('institution', None)
        super().__init__(*args, **kwargs)
        
        # Filter assigned_doctor dropdown only to doctors belonging to this clinic
        if institution:
            self.fields['assigned_doctor'].queryset = User.objects.filter(
                institution=institution,
                role__in=[User.Role.DOCTOR, User.Role.COUNSELOR, User.Role.CLINIC_ADMIN]
            )


class TimelineEventForm(forms.ModelForm):
    class Meta:
        model = PatientTimelineEvent
        fields = ['title', 'description', 'is_visible_to_family']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }