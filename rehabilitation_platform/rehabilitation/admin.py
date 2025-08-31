# admin.py (rehabilitation/admin.py)
from django.contrib import admin
from .models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'date_entree', 'infirmier_referent']
    list_filter = ['user_type', 'date_entree']
    search_fields = ['user__first_name', 'user__last_name']

@admin.register(Objectif)
class ObjectifAdmin(admin.ModelAdmin):
    list_display = ['titre', 'patient', 'categorie', 'est_valide', 'date_creation']
    list_filter = ['categorie', 'est_valide', 'date_creation']
    search_fields = ['titre', 'patient__user__first_name']

@admin.register(SuiviHebdomadaire)
class SuiviHebdomadaireAdmin(admin.ModelAdmin):
    list_display = ['patient', 'semaine', 'humeur', 'motivation', 'participation_activites']
    list_filter = ['semaine', 'humeur', 'motivation']

@admin.register(JournalEntree)
class JournalEntreeAdmin(admin.ModelAdmin):
    list_display = ['patient', 'titre', 'date_creation', 'humeur_jour']
    list_filter = ['date_creation', 'humeur_jour']
    search_fields = ['titre', 'contenu']

@admin.register(CommentaireSoignant)
class CommentaireSoignantAdmin(admin.ModelAdmin):
    list_display = ['patient', 'soignant', 'date_creation', 'prive']
    list_filter = ['date_creation', 'prive', 'soignant__user_type']

@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = ['texte', 'auteur', 'active']
    list_filter = ['active']