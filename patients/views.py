from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Patient, PatientTimelineEvent
from .forms import PatientAdmissionForm, TimelineEventForm
from clinical.models import PatientDailyEntry, Prescription, StatutoryFormRecord, CounselingNote
from billing.models import BillingRecord


@login_required
def patient_list_view(request):
    """
    Tenant-scoped patient directory with search & status filters.
    """
    institution = request.institution
    if request.user.is_superuser and not institution:
        qs = Patient.objects.all()
    elif institution:
        qs = Patient.objects.filter(institution=institution)
    else:
        qs = Patient.objects.none()

    # Search filter
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')

    if q:
        qs = qs.filter(
            Q(full_name__icontains=q) |
            Q(patient_code__icontains=q) |
            Q(phone__icontains=q) |
            Q(addiction_type__icontains=q)
        )
    
    if status_filter:
        qs = qs.filter(status=status_filter)

    context = {
        'patients': qs,
        'search_query': q,
        'current_status': status_filter,
    }
    return render(request, 'patients/patient_list.html', context)


@login_required
def patient_create_view(request):
    """
    Admission intake form. Automatically binds patient to request.institution.
    """
    institution = request.institution

    if request.method == 'POST':
        form = PatientAdmissionForm(request.POST, institution=institution)
        if form.is_valid():
            patient = form.save(commit=False)
            if institution:
                patient.institution = institution
            patient.save()

            # Create initial milestone event on timeline
            PatientTimelineEvent.objects.create(
                patient=patient,
                title="Admission Completed",
                description=f"Admitted under {patient.get_admission_type_display()}.",
                is_visible_to_family=True
            )

            messages.success(request, f"Patient {patient.full_name} admitted successfully! ID: {patient.patient_code}")
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = PatientAdmissionForm(institution=institution)

    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'New Patient Intake'})


@login_required
def patient_detail_view(request, pk):
    """
    Patient Clinical EMR Profile with all tabs (Daily Logs, Prescriptions, Legal Forms, Billing).
    """
    institution = request.institution
    if request.user.is_superuser and not institution:
        patient = get_object_or_404(Patient, pk=pk)
    else:
        patient = get_object_or_404(Patient, pk=pk, institution=institution)

    # Related clinical records
    daily_entries = patient.daily_entries.all()
    prescriptions = patient.prescriptions.all()
    counseling_notes = patient.counseling_notes.all()
    statutory_forms = patient.statutory_forms.all()
    billing_records = patient.billing_records.all()
    timeline_events = patient.timeline_events.all()

    total_billed = sum(b.amount for b in billing_records)
    total_paid = sum(b.amount for b in billing_records if b.is_paid)
    pending_due = total_billed - total_paid

    context = {
        'patient': patient,
        'daily_entries': daily_entries,
        'prescriptions': prescriptions,
        'counseling_notes': counseling_notes,
        'statutory_forms': statutory_forms,
        'billing_records': billing_records,
        'timeline_events': timeline_events,
        'total_billed': total_billed,
        'total_paid': total_paid,
        'pending_due': pending_due,
    }
    return render(request, 'patients/patient_detail.html', context)


def public_family_timeline_view(request, token):
    """
    Publicly accessible family recovery timeline using the unguessable public_token.
    """
    patient = get_object_or_404(Patient, public_token=token)
    timeline = patient.timeline_events.filter(is_visible_to_family=True)

    context = {
        'patient': patient,
        'timeline': timeline,
    }
    return render(request, 'patients/public_timeline.html', context)