from django.shortcuts import render, redirect #render return html template, #redirect - redirect user to antoher url
from django.contrib.auth import login, logout #logs user in, out
from django.contrib.auth.forms import AuthenticationForm #validate username and password
from django.contrib.auth.decorators import login_required #prevents unauthenticated users from accessing a view.
from django.utils import timezone
from django.db.models import Sum
from patients.models import Patient
from billing.models import BillingRecord


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) #s creates the user's authenticated session.
            return redirect('accounts:dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required #This decorator protects the dashboard.
def dashboard_view(request):
    institution = request.institution #from middleware

    # If super admin without assigned clinic, get all; otherwise strictly filter by tenant
    if request.user.is_superuser and not institution: #If the user is a Django superuser AND does not belong to any specific institution.
        patients_qs = Patient.objects.all()
        billing_qs = BillingRecord.objects.all()
    elif institution:
        patients_qs = Patient.objects.filter(institution=institution)
        billing_qs = BillingRecord.objects.filter(patient__institution=institution)
    else:
        patients_qs = Patient.objects.none()
        billing_qs = BillingRecord.objects.none()

    # Dynamic metrics calculation matching TLC Rehab dashboard
    today = timezone.now().date()
    active_patients_count = patients_qs.filter(status=Patient.Status.ACTIVE).count()
    admissions_today_count = patients_qs.filter(admission_date__date=today).count()
    
    bills_ready_count = billing_qs.filter(is_paid=True).count()
    pending_payments_count = billing_qs.filter(is_paid=False).count()

    recent_patients = patients_qs.select_related('assigned_doctor')[:6]

    context = {
        'institution': institution,
        'active_patients_count': active_patients_count,
        'admissions_today_count': admissions_today_count,
        'bills_ready_count': bills_ready_count,
        'pending_payments_count': pending_payments_count,
        'recent_patients': recent_patients,
    }
    return render(request, 'accounts/dashboard.html', context)