from django.db import models
from django.conf import settings
from patients.models import Patient


class PatientDailyEntry(models.Model):
    """
    Daily clinical log recorded by staff/nurses/doctors.
    """
    class RiskLevel(models.TextChoices):
        LOW = 'low', 'Low'
        MODERATE = 'moderate', 'Moderate'
        HIGH = 'high', 'High'
        CRITICAL = 'critical', 'Critical'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='daily_entries')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    kind = models.CharField(max_length=50, default='Daily Round', help_text="e.g. Morning Round, Evening Round")
    
    # Clinical Observations
    mental_condition = models.CharField(max_length=255, blank=True)
    physical_condition = models.CharField(max_length=255, blank=True)
    mood = models.CharField(max_length=100, blank=True)
    withdrawal_symptoms = models.TextField(blank=True)
    sleep_quality = models.CharField(max_length=100, blank=True)
    appetite = models.CharField(max_length=100, blank=True)
    medicines_given = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    risk_level = models.CharField(max_length=20, choices=RiskLevel.choices, default=RiskLevel.LOW)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient.full_name} - {self.kind} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class Prescription(models.Model):
    """
    Active or stopped medical prescriptions.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    prescribed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    medicine_name = models.CharField(max_length=150)
    dosage = models.CharField(max_length=100, help_text="e.g. 50mg, 1 tablet")
    frequency = models.CharField(max_length=100, help_text="e.g. Twice daily (BD), TDS, SOS")
    duration = models.CharField(max_length=100, help_text="e.g. 7 days, 1 month")
    notes = models.TextField(blank=True)
    is_stopped = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine_name} - {self.patient.full_name}"


class MedicineAdministrationLog(models.Model):
    """
    Timestamped nurse/staff log confirming medication was given.
    """
    prescription = models.ForeignKey(
        Prescription, 
        on_delete=models.CASCADE, 
        related_name='administration_logs'
    )
    given_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True
    )
    given_at = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.prescription.medicine_name} given at {self.given_at.strftime('%Y-%m-%d %H:%M')}"


class CounselingNote(models.Model):
    """
    Psychotherapy & counseling session notes.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='counseling_notes')
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    session_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField()

    class Meta:
        ordering = ['-session_date']

    def __str__(self):
        return f"Counseling - {self.patient.full_name} ({self.session_date.strftime('%Y-%m-%d')})"


class StatutoryFormRecord(models.Model):
    """
    Official legal/statutory compliance forms.
    """
    class FormType(models.TextChoices):
        FORM_C = 'formC', 'Form C - Independent Admission [Sec 86]'
        FORM_D = 'formD', 'Form D - Minor Admission [Sec 87]'
        FORM_E = 'formE', 'Form E - High Support Admission [Sec 89]'
        FORM_4 = 'form4', 'Form 4 - Restraint & Seclusion Log'
        FORM_5 = 'form5', 'Form 5 - Suicide Risk Management'
        DAMA = 'dama', 'DAMA - Discharge Against Medical Advice'
        FORM_I = 'formI', 'Form I - Leave of Absence [Sec 91]'
        FORM_J = 'formJ', 'Form J - Police Intimation (Absconding) [Sec 103]'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='statutory_forms')
    form_type = models.CharField(max_length=20, choices=FormType.choices)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    form_data = models.JSONField(default=dict, blank=True, help_text="Stored dynamic JSON key-values of the form")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_form_type_display()} - {self.patient.full_name}"