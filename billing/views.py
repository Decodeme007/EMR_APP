from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from patients.models import Patient
from .models import BillingRecord
from .forms import BillingRecordForm


@login_required
def billing_dashboard_view(request):
    institution = request.institution
    if request.user.is_superuser and not institution:
        bills = BillingRecord.objects.all()
    elif institution:
        bills = BillingRecord.objects.filter(patient__institution=institution)
    else:
        bills = BillingRecord.objects.none()

    total_revenue = sum(b.amount for b in bills if b.is_paid)
    total_pending = sum(b.amount for b in bills if not b.is_paid)

    context = {
        'bills': bills,
        'total_revenue': total_revenue,
        'total_pending': total_pending,
    }
    return render(request, 'billing/billing_dashboard.html', context)


@login_required
def add_billing_record_view(request, patient_id):
    institution = request.institution
    patient = get_object_or_404(Patient, pk=patient_id, institution=institution)

    if request.method == 'POST':
        form = BillingRecordForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.patient = patient
            bill.created_by = request.user
            bill.save()
            messages.success(request, f"Billing entry for ₹{bill.amount} created!")
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = BillingRecordForm()

    return render(request, 'billing/add_bill.html', {'form': form, 'patient': patient})


@login_required
def mark_bill_paid_view(request, bill_id):
    bill = get_object_or_404(BillingRecord, pk=bill_id, patient__institution=request.institution)
    bill.is_paid = True
    bill.payment_type = request.POST.get('payment_type', BillingRecord.PaymentType.CASH)
    bill.save()
    messages.success(request, f"Invoice #{bill.id} marked as Paid via {bill.payment_type}!")
    return redirect('patients:patient_detail', pk=bill.patient.pk)