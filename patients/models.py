import uuid
from django.db import models
from django.conf import settings
from accounts.models import Institution


class Patient(models.Model):
    """
    Main Patient record scoped to a specific Institution (Tenant).
    """
    class AdmissionType(models.TextChoices):
        INDEPENDENT = 'independent', 'Independent Admission (Sec 86)'
        INVOLUNTARY = 'involuntary', 'Involuntary / High Support (Sec 89)'
        MINOR = 'minor', 'Minor Admission (Sec 87)'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Currently Admitted'
        DISCHARGED = 'discharged', 'Discharged'
        TRANSFERRED = 'transferred', 'Transferred'
        DAMA = 'dama', 'Discharged Against Medical Advice (DAMA)'

    # Multi-tenancy link
    institution = models.ForeignKey(
        Institution, 
        on_delete=models.CASCADE, 
        related_name='patients'
    )
    
    # Identification
    patient_code = models.CharField(max_length=50, blank=True, db_index=True)
    public_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # Core Demographics
    full_name = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=20, 
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], 
        default='Male'
    )
    phone = models.CharField(max_length=20, blank=True)
    aadhaar_number = models.CharField(max_length=20, blank=True, verbose_name="Govt ID / Aadhaar")
    address = models.TextField(blank=True)

    # Admission Details
    admission_type = models.CharField(
        max_length=20, 
        choices=AdmissionType.choices, 
        default=AdmissionType.INDEPENDENT
    )
    admission_date = models.DateTimeField()
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.ACTIVE
    )
    addiction_type = models.CharField(
        max_length=100, 
        help_text="e.g. Alcohol, Opioids, Polysubstance, Gambling"
    )
    medical_history = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)

    # Assigned Doctor / Psychiatrist
    assigned_doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_patients'
    )

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=150)
    emergency_contact_phone = models.CharField(max_length=20)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)

    # Guardian / Legal Info (For Minor or Involuntary admissions)
    guardian_name = models.CharField(max_length=150, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)
    guardian_relation = models.CharField(max_length=50, blank=True)
    school_name = models.CharField(max_length=150, blank=True, help_text="For minors")
    grade = models.CharField(max_length=50, blank=True, help_text="For minors")
    legal_reason = models.TextField(blank=True)
    legal_remarks = models.TextField(blank=True)

    # Consents
    self_consent = models.BooleanField(default=False)
    digital_signature = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-admission_date']

    def __str__(self):
        return f"{self.full_name} ({self.patient_code or 'Pending ID'})"

    def save(self, *args, **kwargs):
        """
        Auto-generate patient code with clinic prefix if not already set.
        Example: TLC-01-0001
        """
        if not self.patient_code and self.institution:
            count = Patient.objects.filter(institution=self.institution).count() + 1
            clinic_code = self.institution.code.replace(" ", "").upper()
            self.patient_code = f"{clinic_code}-{count:04d}"
        super().save(*args, **kwargs)


class PatientTimelineEvent(models.Model):
    """
    Chronological milestone events shown on patient profile and family public timeline.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='timeline_events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_visible_to_family = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.patient.full_name}"