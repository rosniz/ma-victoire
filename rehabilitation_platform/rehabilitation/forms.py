# forms.py (rehabilitation/forms.py)
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import *

class ObjectifForm(forms.ModelForm):
    class Meta:
        model = Objectif
        fields = ['titre', 'description', 'categorie']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Ajouter objectif', css_class='btn-primary'))

class SuiviHebdomadaireForm(forms.ModelForm):
    class Meta:
        model = SuiviHebdomadaire
        fields = ['humeur', 'motivation', 'participation_activites', 'douleur_niveau', 'commentaire']
        widgets = {
            'douleur_niveau': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': 1}),
            'commentaire': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enregistrer', css_class='btn-success'))

class JournalEntreeForm(forms.ModelForm):
    class Meta:
        model = JournalEntree
        fields = ['titre', 'contenu', 'image', 'humeur_jour']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Publier', css_class='btn-primary'))

class CommentaireSoignantForm(forms.ModelForm):
    class Meta:
        model = CommentaireSoignant
        fields = ['contenu', 'prive']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Ajouter commentaire', css_class='btn-info'))