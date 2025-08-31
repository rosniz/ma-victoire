# urls.py (rehabilitation/urls.py)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('profil/', views.profil_patient, name='profil'),
    path('profil/<int:patient_id>/', views.profil_patient, name='profil_patient'),
    path('objectifs/', views.objectifs, name='objectifs'),
    path('objectifs/<int:objectif_id>/valider/', views.valider_objectif, name='valider_objectif'),
    path('suivi/', views.suivi_hebdomadaire, name='suivi_hebdomadaire'),
    path('journal/', views.journal, name='journal'),
    path('commentaire/<int:patient_id>/', views.ajouter_commentaire, name='ajouter_commentaire'),
]
