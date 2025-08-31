from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    USER_TYPES = [
        ('patient', 'Patient'),
        ('infirmier', 'Infirmier'),
        ('kine', 'Kinésithérapeute'),
        ('ergo', 'Ergothérapeute'),
        ('psychologue', 'Psychologue'),
        ('medecin', 'Médecin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='patient')
    date_entree = models.DateField(null=True, blank=True)
    infirmier_referent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'user_type': 'infirmier'}
    )
    objectif_principal = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.get_user_type_display()})"

class Objectif(models.Model):
    CATEGORIES = [
        ('emotionnel', '😊 Émotionnel'),
        ('physique', '💪 Physique'),
        ('cognitif', '🧠 Cognitif'),
        ('social', '👥 Social'),
    ]
    
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    date_creation = models.DateTimeField(default=timezone.now)
    est_valide = models.BooleanField(default=False)
    date_validation = models.DateTimeField(null=True, blank=True)
    valide_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.titre} - {self.patient.user.first_name}"

class SuiviHebdomadaire(models.Model):
    HUMEURS = [
        (1, '😢 Très triste'),
        (2, '😟 Triste'),
        (3, '😐 Neutre'),
        (4, '🙂 Content'),
        (5, '😊 Très content'),
    ]
    
    MOTIVATIONS = [
        (1, '❌ Très faible'),
        (2, '😕 Faible'),
        (3, '😐 Moyenne'),
        (4, '😊 Bonne'),
        (5, '✨ Excellente'),
    ]
    
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    semaine = models.DateField()  # Lundi de la semaine
    humeur = models.IntegerField(choices=HUMEURS)
    motivation = models.IntegerField(choices=MOTIVATIONS)
    participation_activites = models.BooleanField(default=False)
    douleur_niveau = models.IntegerField(default=0)  # 0-10
    commentaire = models.TextField(blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['patient', 'semaine']
    
    def __str__(self):
        return f"Suivi {self.patient.user.first_name} - Semaine {self.semaine}"

class JournalEntree(models.Model):
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200, blank=True)
    contenu = models.TextField()
    image = models.ImageField(upload_to='journal/', null=True, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    humeur_jour = models.IntegerField(choices=SuiviHebdomadaire.HUMEURS, null=True, blank=True)
    
    class Meta:
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Journal {self.patient.user.first_name} - {self.date_creation.strftime('%d/%m/%Y')}"

class CommentaireSoignant(models.Model):
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='commentaires_recus')
    soignant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='commentaires_donnes')
    contenu = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)
    prive = models.BooleanField(default=False)  # Visible seulement par l'équipe
    
    class Meta:
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Commentaire de {self.soignant.user.first_name} pour {self.patient.user.first_name}"

class Citation(models.Model):
    texte = models.TextField()
    auteur = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.texte[:50]}..."