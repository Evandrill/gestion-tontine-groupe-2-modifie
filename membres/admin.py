from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.db.models import Sum

from membres.models import Membre
from tontines.models import Tontine, Cycle, MembreTontine, Attribution
from operations.models import Cotisation, Pret, Remboursement, Don
from utilisateurs.models import CustomUser  # Modèle utilisateur personnalisé
from django.shortcuts import render


class CustomAdminSite(admin.AdminSite):
    site_header = "Tableau de bord Tontine"
    site_title = "Administration Tontine"
    index_title = "Statistiques et Activités Récentes"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.dashboard_view), name='index'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Statistiques clés
        stats = {
            'total_membres': Membre.objects.count(),
            'total_tontines': Tontine.objects.count(),
            'total_prets': Pret.objects.count(),
            'total_cotisations': Cotisation.objects.count(),
            'total_dons': Don.objects.count(),
            'total_remboursements': Remboursement.objects.count(),
            'total_utilisateurs': CustomUser.objects.count(),
        }

        # Derniers prêts (5)
        derniers_prets = Pret.objects.select_related('membre', 'tontine').order_by('-date_demande')[:5]

        # Derniers dons (5)
        derniers_dons = Don.objects.select_related('tontine', 'donateur').order_by('-date_don')[:5]

        context = dict(
            self.each_context(request),
            stats=stats,
            derniers_prets=derniers_prets,
            derniers_dons=derniers_dons,
        )
        return render(request, 'admin/dashboard.html', context) 

# Instanciation du site admin personnalisé
custom_admin_site = CustomAdminSite(name='customadmin')


# ModelAdmin pour Membre
class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone', 'email', 'statut')
    search_fields = ('nom', 'prenom', 'email', 'telephone')
    list_filter = ('statut',)
    

# ModelAdmin pour Tontine
class TontineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'montant_cotisation', 'frequence_cotisation', 'est_active')
    list_filter = ('est_active', 'frequence_cotisation')
    search_fields = ('nom',)


# ModelAdmin pour CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('username', 'email')


# Enregistrements dans l’admin personnalisé
custom_admin_site.register(Membre, MembreAdmin)
custom_admin_site.register(Tontine, TontineAdmin)
custom_admin_site.register(CustomUser, CustomUserAdmin)
custom_admin_site.register(Cycle)
custom_admin_site.register(MembreTontine)
custom_admin_site.register(Attribution)
custom_admin_site.register(Cotisation)
custom_admin_site.register(Pret)
custom_admin_site.register(Remboursement)
custom_admin_site.register(Don)



