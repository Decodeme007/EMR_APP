from django.db import models
from django.conf import settings
from patients.models import Patient


class BillingRecord(models.Model):
    """
    Billing items and payment tracking for a patient.
    """
    class PaymentType(models.TextChoices):
        CASH = 'Cash', 'Cash'
        UPI = 'UPI', 'UPI / Online'
        CARD = 'Card', 'Credit / Debit Card'
        BANK_TRANSFER = 'Bank Transfer', 'Bank Transfer'
        PENDING = 'Pending', 'Pending / Unpaid'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='billing_records')
    item = models.CharField(max_length=200, help_text="e.g. Admission Fee, Therapy Session, Bed Charges")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_type = models.CharField(
        max_length=50, 
        choices=PaymentType.choices, 
        default=PaymentType.PENDING
    )
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.item} - ₹{self.amount} ({'Paid' if self.is_paid else 'Unpaid'})"