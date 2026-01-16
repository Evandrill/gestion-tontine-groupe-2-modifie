from django import forms
from .models import Cotisation, Pret, Remboursement, Don
from demandes.models import DemandeCotisation, DemandeDon, DemandePret, AdhesionTontineDemande

class CotisationForm(forms.ModelForm):
    class Meta:
        model = Cotisation
        fields = ('membre', 'tontine', 'cycle', 'montant', 'date_prevue', 'est_payee', 'commentaire')
        widgets = {
            'date_prevue': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from demandes.models import DemandePret

class PretDemandeForm(forms.ModelForm):
    class Meta:
        model = DemandePret
        fields = ['montant']


class CotisationDemandeForm(forms.ModelForm):  # anciennement DemandeCotisationForm
    class Meta:
        model = DemandeCotisation
        fields = ['montant']


class DemandeAdhesionTontineForm(forms.ModelForm):
    class Meta:
        model = AdhesionTontineDemande
        fields = ['tontine']

class DemandeDonForm(forms.ModelForm):
    class Meta:
        model = DemandeDon
        fields = ['montant', 'motif']

class PretForm(forms.ModelForm):
    class Meta:
        model = Pret
        fields = ('membre', 'tontine', 'montant', 'taux_interet', 'date_echeance', 'statut', 'cni_justificatif')
        widgets = {
            'date_echeance': forms.DateInput(attrs={'type': 'date'}),
        }
class RemboursementForm(forms.ModelForm):
    class Meta:
        model = Remboursement
        fields = ('pret', 'montant', 'commentaire')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pret'].queryset = Pret.objects.filter(statut='EN_COURS')

from django import forms
from .models import Don

class DonForm(forms.ModelForm):
    class Meta:
        model = Don
        fields = ['donateur', 'beneficiaire', 'montant', 'date_don', 'tontine', 'sens_don', 'motif']
        widgets = {
            'date_don': forms.DateInput(attrs={'type': 'date'}),
        }


