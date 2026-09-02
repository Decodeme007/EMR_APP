from django.urls import path
from . import views

app_name = 'clinical'

urlpatterns = [
    path('patient/<int:patient_id>/daily-entry/', views.add_daily_entry_view, name='add_daily_entry'),
    path('patient/<int:patient_id>/prescription/', views.add_prescription_view, name='add_prescription'),
    path('prescription/<int:prescription_id>/administer/', views.administer_medicine_view, name='administer_medicine'),
    path('patient/<int:patient_id>/counseling/', views.add_counseling_note_view, name='add_counseling_note'),
    path('patient/<int:patient_id>/statutory-form/', views.add_statutory_form_view, name='add_statutory_form'),
]