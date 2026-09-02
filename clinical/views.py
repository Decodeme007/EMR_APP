from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from patients.models import Patient
from .models import PatientDailyEntry, Prescription, MedicineAdministrationLog, CounselingNote, StatutoryFormRecord
from .forms import PatientDailyEntryForm, PrescriptionForm, CounselingNoteForm, StatutoryFormRecordForm


@login_required
def add_daily_entry_view(request, patient_id):
    institution = request.institution
    patient = get_object_or_404(Patient, pk=patient_id, institution=institution)

    if request.method == 'POST':
        form = PatientDailyEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.patient = patient
            entry.created_by = request.user
            entry.save()
            messages.success(request, "Daily clinical round logged successfully!")
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = PatientDailyEntryForm()

    return render(request, 'clinical/add_daily_entry.html', {'form': form, 'patient': patient})


@login_required
def add_prescription_view(request, patient_id):
    institution = request.institution
    patient = get_object_or_404(Patient, pk=patient_id, institution=institution)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            rx = form.save(commit=False)
            rx.patient = patient
            rx.prescribed_by = request.user
            rx.save()
            messages.success(request, f"Prescription for {rx.medicine_name} added!")
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = PrescriptionForm()

    return render(request, 'clinical/add_prescription.html', {'form': form, 'patient': patient})


@login_required
def administer_medicine_view(request, prescription_id):
    """
    Nurse/Staff 1-click action confirming medicine was administered.
    """
    rx = get_object_or_404(Prescription, pk=prescription_id, patient__institution=request.institution)
    MedicineAdministrationLog.objects.create(
        prescription=rx,
        given_by=request.user,
        remarks=request.POST.get('remarks', 'Administered as scheduled')
    )
    messages.success(request, f"Recorded administration for {rx.medicine_name}!")
    return redirect('patients:patient_detail', pk=rx.patient.pk)


@login_required
def add_counseling_note_view(request, patient_id):
    institution = request.institution
    patient = get_object_or_404(Patient, pk=patient_id, institution=institution)

    if request.method == 'POST':
        form = CounselingNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.patient = patient
            note.counselor = request.user
            note.save()
            messages.success(request, "Counseling session note added!")
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = CounselingNoteForm()

    return render(request, 'clinical/add_counseling_note.html', {'form': form, 'patient': patient})


@login_required
def add_statutory_form_view(request, patient_id):
    institution = request.institution
    patient = get_object_or_404(Patient, pk=patient_id, institution=institution)

    if request.method == 'POST':
        form = StatutoryFormRecordForm(request.POST)
        if form.is_valid():
            s_form = form.save(commit=False)
            s_form.patient = patient
            s_form.created_by = request.user
            s_form.save()
            messages.success(request, f"Statutory {s_form.get_form_type_display()} recorded!")
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = StatutoryFormRecordForm()

    return render(request, 'clinical/add_statutory_form.html', {'form': form, 'patient': patient})