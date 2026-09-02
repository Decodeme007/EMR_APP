from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patient_list_view, name='patient_list'),
    path('new-admission/', views.patient_create_view, name='patient_create'),
    path('<int:pk>/', views.patient_detail_view, name='patient_detail'),
    path('timeline/<uuid:token>/', views.public_family_timeline_view, name='public_timeline'),
]