# views.py (rehabilitation/views.py)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import datetime, timedelta
import random
from .models import *
from .forms import *

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Créer le profil utilisateur
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    profile = request.user.userprofile
    citation = None
    
    # Citation motivante aléatoire
    citations = Citation.objects.filter(active=True)
    if citations.exists():
        citation = random.choice(citations)
    
    context = {
        'profile': profile,
        'citation': citation,
    }
    
    if profile.user_type == 'patient':
        # Dashboard patient
        objectifs = Objectif.objects.filter(patient=profile)
        journal_entries = JournalEntree.objects.filter(patient=profile)[:5]
        suivi_recent = SuiviHebdomadaire.objects.filter(patient=profile).order_by('-semaine')[:4]
        
        context.update({
            'objectifs': objectifs,
            'objectifs_valides': objectifs.filter(est_valide=True).count(),
            'objectifs_total': objectifs.count(),
            'journal_entries': journal_entries,
            'suivi_recent': suivi_recent,
        })
        return render(request, 'rehabilitation/dashboard_patient.html', context)
    
    else:
        # Dashboard soignant
        if profile.user_type == 'infirmier':
            patients = UserProfile.objects.filter(infirmier_referent=profile)
        else:
            patients = UserProfile.objects.filter(user_type='patient')
        
        context.update({
            'patients': patients,
            'nb_patients': patients.count(),
        })
        return render(request, 'rehabilitation/dashboard_soignant.html', context)

@login_required
def profil_patient(request, patient_id=None):
    if patient_id:
        # Vue soignant regardant un patient
        patient = get_object_or_404(UserProfile, id=patient_id, user_type='patient')
        if request.user.userprofile.user_type == 'patient':
            return redirect('dashboard')
    else:
        # Vue patient de son propre profil
        patient = request.user.userprofile
        if patient.user_type != 'patient':
            return redirect('dashboard')
    
    objectifs = Objectif.objects.filter(patient=patient)
    commentaires = CommentaireSoignant.objects.filter(patient=patient)
    
    # Si c'est un patient qui regarde son profil, masquer les commentaires privés
    if request.user.userprofile == patient:
        commentaires = commentaires.filter(prive=False)
    
    context = {
        'patient': patient,
        'objectifs': objectifs,
        'commentaires': commentaires,
        'peut_modifier': request.user.userprofile == patient or request.user.userprofile.user_type != 'patient',
    }
    return render(request, 'rehabilitation/profil_patient.html', context)

@login_required
def objectifs(request):
    profile = request.user.userprofile
    
    if request.method == 'POST':
        form = ObjectifForm(request.POST)
        if form.is_valid():
            objectif = form.save(commit=False)
            objectif.patient = profile
            objectif.save()
            messages.success(request, 'Objectif ajouté avec succès!')
            return redirect('objectifs')
    else:
        form = ObjectifForm()
    
    objectifs = Objectif.objects.filter(patient=profile)
    
    return render(request, 'rehabilitation/objectifs.html', {
        'objectifs': objectifs,
        'form': form,
    })

@login_required
def valider_objectif(request, objectif_id):
    objectif = get_object_or_404(Objectif, id=objectif_id)
    
    # Seul le patient ou un soignant peut valider
    if request.user.userprofile == objectif.patient or request.user.userprofile.user_type != 'patient':
        objectif.est_valide = not objectif.est_valide
        if objectif.est_valide:
            objectif.date_validation = timezone.now()
            objectif.valide_par = request.user
        else:
            objectif.date_validation = None
            objectif.valide_par = None
        objectif.save()
        
        messages.success(request, 'Objectif mis à jour!')
    
    return redirect('objectifs')

@login_required
def suivi_hebdomadaire(request):
    profile = request.user.userprofile
    
    if profile.user_type != 'patient':
        return redirect('dashboard')
    
    # Semaine courante (lundi)
    today = timezone.now().date()
    lundi = today - timedelta(days=today.weekday())
    
    suivi_actuel, created = SuiviHebdomadaire.objects.get_or_create(
        patient=profile,
        semaine=lundi,
        defaults={
            'humeur': 3,
            'motivation': 3,
            'participation_activites': False,
            'douleur_niveau': 0,
        }
    )
    
    if request.method == 'POST':
        form = SuiviHebdomadaireForm(request.POST, instance=suivi_actuel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Suivi hebdomadaire mis à jour!')
            return redirect('suivi_hebdomadaire')
    else:
        form = SuiviHebdomadaireForm(instance=suivi_actuel)
    
    # Historique des 8 dernières semaines
    historique = SuiviHebdomadaire.objects.filter(
        patient=profile
    ).order_by('-semaine')[:8]
    
    return render(request, 'rehabilitation/suivi_hebdomadaire.html', {
        'form': form,
        'suivi_actuel': suivi_actuel,
        'historique': historique,
    })

@login_required
def journal(request):
    profile = request.user.userprofile
    
    if profile.user_type != 'patient':
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = JournalEntreeForm(request.POST, request.FILES)
        if form.is_valid():
            entree = form.save(commit=False)
            entree.patient = profile
            entree.save()
            messages.success(request, 'Entrée de journal ajoutée!')
            return redirect('journal')
    else:
        form = JournalEntreeForm()
    
    entries = JournalEntree.objects.filter(patient=profile)
    
    return render(request, 'rehabilitation/journal.html', {
        'entries': entries,
        'form': form,
    })

@login_required
def ajouter_commentaire(request, patient_id):
    if request.user.userprofile.user_type == 'patient':
        return redirect('dashboard')
    
    patient = get_object_or_404(UserProfile, id=patient_id, user_type='patient')
    
    if request.method == 'POST':
        form = CommentaireSoignantForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.patient = patient
            commentaire.soignant = request.user.userprofile
            commentaire.save()
            messages.success(request, 'Commentaire ajouté!')
    
    return redirect('profil_patient', patient_id=patient_id)