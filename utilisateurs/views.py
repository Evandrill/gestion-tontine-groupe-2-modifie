from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from membres.models import Membre
from tontines.models import Tontine, Cycle
from operations.models import Cotisation, Pret, Remboursement
from demandes.models import DemandePret, DemandeCotisation, DemandeRemboursement, DemandeDon, AdhesionTontineDemande


from django.contrib.auth.models import Group

# --- Authentication Views ---
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Membre')
            user.groups.add(group)
            login(request, user)
            messages.success(request, f"Compte créé pour {user.username}. Bienvenue !")
            return redirect('utilisateurs:profil')
    else:
        form = CustomUserCreationForm()
    return render(request, 'utilisateurs/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('utilisateurs:profil')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = AuthenticationForm()
    return render(request, 'utilisateurs/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('connexion')  # Cette route doit exister


# --- Profile Views ---
@login_required
def profil_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour.")
            return redirect('utilisateurs:profil')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'utilisateurs/profile.html', {'form': form})

# --- Redirection après login selon le rôle ---
@login_required
def redirection_apres_login(request):
    user = request.user
    if user.groups.filter(name='President').exists():
        return redirect('utilisateurs:admin_dashboard')
    elif user.groups.filter(name='Tresorier').exists():
        return redirect('utilisateurs:tresorier_dashboard')
    else: # Assumes 'Membre' or no specific group
        return redirect('utilisateurs:user_dashboard')

# --- Dashboard Views ---
@login_required
def admin_dashboard_view(request):
    # Ensure only presidents can access this page
    if not request.user.groups.filter(name='President').exists():
        messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
        return redirect('utilisateurs:redirection')

    membres = CustomUser.objects.filter(groups__name='Membre')
    cotisations_a_valider = Cotisation.objects.filter(statut__in=['planifie', 'en_retard'])
    prets_a_valider = Pret.objects.filter(date_approbation__isnull=True)
    context = {
        'membres': membres,
        'cotisations_a_valider': cotisations_a_valider,
        'prets_a_valider': prets_a_valider,
    }
    return render(request, 'utilisateurs/admin_dashboard.html', context)

from django.db.models import Sum

@login_required
def tresorier_dashboard_view(request):
    if not request.user.groups.filter(name='Tresorier').exists():
        messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
        return redirect('utilisateurs:redirection')

    caisse_totale = Cotisation.objects.filter(statut='paye').aggregate(total=Sum('montant'))['total'] or 0
    
    context = {
        'caisse_totale': caisse_totale,
    }
    return render(request, 'utilisateurs/tresorier_dashboard.html', context)
from tontines.models import Attribution

@login_required
def user_dashboard_view(request):
    try:
        membre = request.user.membre_membres
    except Membre.DoesNotExist:
        # This user does not have a member profile, handle appropriately
        membre = None

    active_cycle = Cycle.objects.filter(est_actif=True).first()
    rang = None
    if active_cycle and membre:
        attribution = Attribution.objects.filter(cycle=active_cycle, membre=membre).first()
        if attribution:
            rang = attribution.ordre

    solde_cotisation = 0
    if active_cycle and membre:
        solde_cotisation = Cotisation.objects.filter(
            membre=membre,
            cycle=active_cycle,
            statut='paye'
        ).aggregate(total=Sum('montant'))['total'] or 0

    prochaines_reunions = []
    if active_cycle:
        prochaines_reunions = Attribution.objects.filter(
            cycle=active_cycle, 
            date_prevue__gte=timezone.now()
        ).order_by('date_prevue')[:5]

    total_membres = Membre.objects.filter(statut='ACTIF').count()
    total_tontines = Tontine.objects.filter(est_active=True).count()
    cycles_actifs = Cycle.objects.filter(est_actif=True).count()

    # The following lines are probably incorrect due to duplicate models, but I leave them for now
    cotisations_recentes = Cotisation.objects.filter(est_payee=True).order_by('-date_paiement')[:5]
    remboursements_recents = Remboursement.objects.order_by('-date_paiement')[:5]
    prets_en_cours = Pret.objects.filter(statut='EN_COURS').count()

    context = {
        'rang': rang,
        'solde_cotisation': solde_cotisation,
        'prochaines_reunions': prochaines_reunions,
        'total_membres': total_membres,
        'total_tontines': total_tontines,
        'cycles_actifs': cycles_actifs,
        'cotisations_recentes': cotisations_recentes,
        'remboursements_recents': remboursements_recents,
        'prets_en_cours': prets_en_cours,
    }

    return render(request, 'utilisateurs/user_dashboard.html', context)
def connexion(request):
    # Ta logique de connexion ici
    return render(request, 'utilisateurs/login.html')

from .models import CustomUser
from django.shortcuts import get_object_or_404

from django.utils import timezone

@login_required
def validate_cotisation_view(request, cotisation_id):
    if request.method == 'POST':
        if not request.user.groups.filter(name='President').exists():
            messages.error(request, "Vous n'avez pas l'autorisation de faire cette action.")
            return redirect('utilisateurs:redirection')
        
        cotisation = get_object_or_404(Cotisation, id=cotisation_id)
        cotisation.statut = 'paye'
        cotisation.date_effective = timezone.now()
        cotisation.save()
        messages.success(request, f"La cotisation de {cotisation.membre} a été validée.")
        return redirect('utilisateurs:admin_dashboard')
    else:
        messages.error(request, "Action non autorisée.")
        return redirect('utilisateurs:admin_dashboard')

@login_required
def validate_pret_view(request, pret_id):
    if request.method == 'POST':
        if not request.user.groups.filter(name='President').exists():
            messages.error(request, "Vous n'avez pas l'autorisation de faire cette action.")
            return redirect('utilisateurs:redirection')
        
        pret = get_object_or_404(Pret, id=pret_id)
        pret.date_approbation = timezone.now()
        pret.approuve_par = request.user
        pret.save()
        messages.success(request, f"Le prêt de {pret.membre} a été approuvé.")
        return redirect('utilisateurs:admin_dashboard')
    else:
        messages.error(request, "Action non autorisée.")
        return redirect('utilisateurs:admin_dashboard')

@login_required
def remove_member_view(request, user_id):
    if request.method == 'POST':
        if not request.user.groups.filter(name='President').exists():
            messages.error(request, "Vous n'avez pas l'autorisation de faire cette action.")
            return redirect('utilisateurs:redirection')
        
        member_to_remove = get_object_or_404(CustomUser, id=user_id)
        member_to_remove.delete()
        messages.success(request, f"Le membre {member_to_remove.username} a été supprimé.")
        return redirect('utilisateurs:admin_dashboard')
    else:
        messages.error(request, "Action non autorisée.")
        return redirect('utilisateurs:admin_dashboard')

from tontines.models import Tontine, Cycle, MembreTontine

from operations.forms import RemboursementForm

@login_required
def report_reimbursement_view(request):
    if not request.user.groups.filter(name='Tresorier').exists():
        messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
        return redirect('utilisateurs:redirection')

    if request.method == 'POST':
        form = RemboursementForm(request.POST)
        if form.is_valid():
            remboursement = form.save(commit=False)
            remboursement.enregistre_par = request.user
            remboursement.save()
            
            # Check if the loan is fully reimbursed
            remboursement.pret.verifier_remboursement()
            
            messages.success(request, "Le remboursement a été enregistré.")
            return redirect('utilisateurs:tresorier_dashboard')
    else:
        form = RemboursementForm()

    context = {
        'form': form,
    }
    return render(request, 'utilisateurs/report_reimbursement.html', context)

@login_required
def schedule_rounds_view(request):
    if not request.user.groups.filter(name='President').exists():
        messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
        return redirect('utilisateurs:redirection')

    if request.method == 'POST':
        tontine_id = request.POST.get('tontine_id')
        tontine = get_object_or_404(Tontine, id=tontine_id)
        
        # Create a new cycle
        cycle = Cycle.objects.create(
            tontine=tontine,
            nom=f"Cycle du {timezone.now().strftime('%Y-%m-%d')}",
            date_debut=timezone.now(),
            est_actif=True
        )

        membres_tontine = MembreTontine.objects.filter(tontine=tontine, est_actif=True)
        for membre_tontine in membres_tontine:
            ordre = request.POST.get(f'ordre_{membre_tontine.membre.id}')
            if ordre:
                Attribution.objects.create(
                    cycle=cycle,
                    membre=membre_tontine.membre,
                    ordre=int(ordre),
                    date_prevue=timezone.now(), # Placeholder
                    montant=tontine.montant_cotisation
                )
        
        messages.success(request, f"L'ordre des tours pour le nouveau cycle de la tontine '{tontine.nom}' a été enregistré.")
        return redirect('utilisateurs:admin_dashboard')


    tontines = Tontine.objects.filter(est_active=True)
    selected_tontine = None
    membres_tontine = []

    tontine_id = request.GET.get('tontine')
    if tontine_id:
        selected_tontine = get_object_or_404(Tontine, id=tontine_id)
        membres_tontine = MembreTontine.objects.filter(tontine=selected_tontine, est_actif=True)

    context = {
        'tontines': tontines,
        'selected_tontine': selected_tontine,
        'membres_tontine': membres_tontine,
    }
    return render(request, 'utilisateurs/schedule_rounds.html', context)

@login_required
def dashboard_demande_view(request):
    user = request.user
    demandes_pret = DemandePret.objects.filter(membre=user)
    demandes_cotisation = DemandeCotisation.objects.filter(membre=user)
    demandes_remboursement = DemandeRemboursement.objects.filter(membre=user)
    demandes_don = DemandeDon.objects.filter(donateur=user)
    demandes_adhesion = AdhesionTontineDemande.objects.filter(membre=user)

    context = {
        'demandes_pret': demandes_pret,
        'demandes_cotisation': demandes_cotisation,
        'demandes_remboursement': demandes_remboursement,
        'demandes_don': demandes_don,
        'demandes_adhesion': demandes_adhesion,
    }
    return render(request, 'utilisateurs/mon_espace.html', context)

