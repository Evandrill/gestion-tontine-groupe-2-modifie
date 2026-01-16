from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from operations import views as operations_views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from utilisateurs.views import profil_view
from membres.admin import custom_admin_site 
urlpatterns = [
    # Admin
   
    # Redirection de la racine vers la page de login
    path('', lambda request: redirect('utilisateurs:login')),
    # Applications principales
    path('utilisateurs/', include('utilisateurs.urls')),
    path('membres/', include('membres.urls')),
    path('tontines/', include(('tontines.urls', 'tontines'), namespace='tontines')),
    path('prets/', include('prets.urls')),
    path('remboursements/', include('remboursements.urls')),
    path('cotisations/', include('cotisations.urls')),
    path('dons/', include('dons.urls')),
    path('operations/', include('operations.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('admin/', custom_admin_site.urls),

    # Nous retirons ces routes en double pour éviter la confusion
    # path('login/', auth_views.LoginView.as_view(template_name='utilisateurs/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Auth Django (optionnel si tu veux utiliser les vues login/logout/password de base)
   

    # Routes spécifiques aux opérations
    path('operations/cotisations/enregistrer/', operations_views.enregistrer_cotisation, name='enregistrer_cotisation'),
    path('operations/cotisations/', operations_views.liste_cotisations, name='liste_cotisations'),

    path('operations/prets/enregistrer/', operations_views.enregistrer_pret, name='enregistrer_pret'),
    path('operations/prets/', operations_views.liste_prets, name='liste_prets'),
    path('operations/prets/<int:pret_id>/', operations_views.detail_pret, name='detail_pret'),

    path('operations/remboursements/enregistrer/<int:pret_id>/', operations_views.enregistrer_remboursement, name='enregistrer_remboursement'),
    path('operations/remboursements/', operations_views.liste_remboursements, name='liste_remboursements'),

    path('operations/dons/enregistrer/', operations_views.enregistrer_don, name='enregistrer_don'),
    path('operations/dons/', operations_views.liste_dons, name='liste_dons'),
    path('profile/', profil_view, name='profile'),

]

# Pour les fichiers statiques en mode développement
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)