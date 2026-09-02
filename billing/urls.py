from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.billing_dashboard_view, name='billing_dashboard'),
    path('patient/<int:patient_id>/add-bill/', views.add_billing_record_view, name='add_bill'),
    path('bill/<int:bill_id>/mark-paid/', views.mark_bill_paid_view, name='mark_paid'),
]