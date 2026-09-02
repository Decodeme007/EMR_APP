from django.db import models #this gives django charField, email field , foreignkey 
from django.contrib.auth.models import AbstractUser #default user model contails username, password, is_staff, active,last_login etc


class Institution(models.Model): #represtnt one clinic
    """
    Tenant Model: Represents each Rehab Clinic / Facility.
    Every clinic has isolated patients, logs, and users.
    """
    SUBSCRIPTION_CHOICES = [
        ('Basic', 'Basic'),
        ('Pro', 'Pro'),
        ('Enterprise', 'Enterprise'),
    ]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, help_text="e.g. TLC-01")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='clinic_logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    subscription_tier = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default='Enterprise')
    
    # Custom SMTP details for clinic automated emails/notifications
    smtp_email = models.CharField(max_length=200, blank=True)
    smtp_app_password = models.CharField(max_length=200, blank=True)
    sender_display_name = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): #This controls how the object appears in Django Admin and debugging.
        return f"{self.name} ({self.code})"


class User(AbstractUser):
    """
    Custom User supporting role-based permissions scoped to an Institution.
    """
    class Role(models.TextChoices): #define allowed choices (nested class)
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin (System Owner)'
        CLINIC_ADMIN = 'CLINIC_ADMIN', 'Clinic Administrator'
        DOCTOR = 'DOCTOR', 'Doctor / Psychiatrist'
        COUNSELOR = 'COUNSELOR', 'Counselor / Therapist'
        CLINICAL_STAFF = 'CLINICAL_STAFF', 'Clinical Staff / Nurse'
        RECEPTIONIST = 'RECEPTIONIST', 'Receptionist'

    institution = models.ForeignKey( #One Institution → Many Users
        Institution,
        on_delete=models.CASCADE, #insitute delete -> all user related to it also deleted
        related_name='users',
        null=True, #done for super admin he doesn't belong to any one insitute - database - null
        blank=True, ##done for super admin he doesn't belong to any one insitute - can send blank
        help_text="Tenant clinic. Super Admins can have this blank."
    )
    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.CLINICAL_STAFF
    )
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()} ({self.institution.name if self.institution else 'Global'})"

    @property #noramlly a function is called with paramerter but because of property you can use it like variable
    def is_doctor_or_therapist(self):
        return self.role in [self.Role.DOCTOR, self.Role.COUNSELOR]

    @property
    def is_admin_or_manager(self):
        return self.role in [self.Role.SUPER_ADMIN, self.Role.CLINIC_ADMIN]

'''
Python Class
     ↓
Django Model
     ↓
Database Table
     ↓
Each Row becomes a Model Object
'''