from django import forms
from .models import BillingRecord


class BillingRecordForm(forms.ModelForm):
    class Meta:
        model = BillingRecord
        fields = ['item', 'amount', 'is_paid', 'payment_type', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 2}),
        }