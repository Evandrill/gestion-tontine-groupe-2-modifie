# GUIDE D'UTILISATION - Application Gestion Tontine

## VERIFICATION DES FONCTIONNALITES DEMANDEES

| Fonctionnalite demandee | Statut | Localisation |
|------------------------|--------|--------------|
| Interface login | OK | `/utilisateurs/login/` |
| Creer un compte | OK | `/utilisateurs/register/` |
| 3 roles (President, Tresorier, Membre) | OK | Migration `0006_create_groups.py` |
| **PRESIDENT** | | |
| - Liste des membres | OK | `admin_dashboard.html` |
| - Ajouter un membre | OK | Lien vers register |
| - Retirer un membre | OK | Bouton "Retirer" |
| - Valider les cotisations | OK | Section "Cotisations a Valider" |
| - Valider les prets | OK | Section "Prets a Valider" |
| - Programmer l'ordre des tours | OK | `/utilisateurs/schedule_rounds/` |
| **TRESORIER** | | |
| - Voir la caisse totale | OK | `tresorier_dashboard.html` |
| - Signaler les remboursements | OK | `/utilisateurs/report_reimbursement/` |
| **MEMBRE** | | |
| - Voir son rang dans le tour | OK | `user_dashboard.html` |
| - Voir les dates de reunion | OK | Section "Prochaines Reunions" |
| - Voir le solde de cotisation | OK | Section "Solde de mes Cotisations" |

---

## 1. LANCER L'APPLICATION

```bash
# Ouvrir un terminal dans le dossier du projet
cd /chemin/vers/gestion-tontine-groupe-2

# 1. Migrer la base de donnees (cree les 3 groupes automatiquement)
python manage.py migrate

# 2. Creer un superutilisateur (si pas encore fait)
python manage.py createsuperuser

# 3. Lancer le serveur
python manage.py runserver
```

---

## 2. CREER LES UTILISATEURS DE TEST

### Option A : Via Django Admin (PLUS SIMPLE)

1. Allez sur `http://127.0.0.1:8000/admin/`
2. Connectez-vous avec le superutilisateur

#### Creer un President :
1. **Utilisateurs** > **Ajouter**
2. Username : `president` | Password : `Test1234!`
3. **Enregistrer et continuer les modifications**
4. Descendez jusqu'a **Groupes**
5. Dans la liste de gauche, selectionnez **President**
6. Cliquez sur la fleche **>** pour l'ajouter a droite
7. **Enregistrer**

#### Creer un Tresorier :
1. **Utilisateurs** > **Ajouter**
2. Username : `tresorier` | Password : `Test1234!`
3. **Enregistrer et continuer les modifications**
4. Descendez jusqu'a **Groupes**
5. Selectionnez **Tresorier** et cliquez **>**
6. **Enregistrer**

#### Creer un Membre :
1. **Utilisateurs** > **Ajouter**
2. Username : `membre1` | Password : `Test1234!`
3. **Enregistrer et continuer les modifications**
4. Descendez jusqu'a **Groupes**
5. Selectionnez **Membre** et cliquez **>**
6. **Enregistrer**

### Option B : Via le Shell Django (PLUS RAPIDE)

```bash
python manage.py shell
```

Copiez-collez ce code :

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# S'assurer que les groupes existent
Group.objects.get_or_create(name='President')
Group.objects.get_or_create(name='Tresorier')
Group.objects.get_or_create(name='Membre')

# Creer President
if not User.objects.filter(username='president').exists():
    u = User.objects.create_user('president', password='Test1234!')
    u.groups.add(Group.objects.get(name='President'))
    print("President cree!")

# Creer Tresorier
if not User.objects.filter(username='tresorier').exists():
    u = User.objects.create_user('tresorier', password='Test1234!')
    u.groups.add(Group.objects.get(name='Tresorier'))
    print("Tresorier cree!")

# Creer Membre
if not User.objects.filter(username='membre1').exists():
    u = User.objects.create_user('membre1', password='Test1234!')
    u.groups.add(Group.objects.get(name='Membre'))
    print("Membre cree!")

# Afficher tous les utilisateurs
print("\n=== UTILISATEURS ===")
for u in User.objects.all():
    groupes = [g.name for g in u.groups.all()]
    print(f"  {u.username} -> {groupes if groupes else 'Aucun groupe'}")
```

Tapez `exit()` pour quitter.

---

## 3. TESTER CHAQUE INTERFACE

### URLs importantes

| Page | URL |
|------|-----|
| Connexion | `http://127.0.0.1:8000/utilisateurs/login/` |
| Inscription | `http://127.0.0.1:8000/utilisateurs/register/` |
| Redirection auto selon role | `http://127.0.0.1:8000/utilisateurs/redirection/` |
| Dashboard President | `http://127.0.0.1:8000/utilisateurs/admin_dashboard/` |
| Dashboard Tresorier | `http://127.0.0.1:8000/utilisateurs/tresorier_dashboard/` |
| Dashboard Membre | `http://127.0.0.1:8000/utilisateurs/user_dashboard/` |
| Programmer les tours | `http://127.0.0.1:8000/utilisateurs/schedule_rounds/` |
| Signaler remboursement | `http://127.0.0.1:8000/utilisateurs/report_reimbursement/` |

### Test President
1. Allez sur `http://127.0.0.1:8000/utilisateurs/login/`
2. Connectez-vous : `president` / `Test1234!`
3. Allez sur `http://127.0.0.1:8000/utilisateurs/redirection/`
4. Vous etes redirige vers le **Dashboard President**

**Fonctionnalites disponibles :**
- Liste des membres avec bouton "Retirer"
- Lien "Ajouter un membre"
- Tableau des cotisations a valider avec bouton "Valider"
- Tableau des prets a valider avec bouton "Approuver"
- Lien "Programmer les tours"

### Test Tresorier
1. Deconnectez-vous ou ouvrez une fenetre privee
2. Connectez-vous : `tresorier` / `Test1234!`
3. Allez sur `http://127.0.0.1:8000/utilisateurs/redirection/`
4. Vous etes redirige vers le **Dashboard Tresorier**

**Fonctionnalites disponibles :**
- Caisse totale (somme des cotisations payees)
- Bouton "Signaler un remboursement"

### Test Membre
1. Deconnectez-vous ou ouvrez une fenetre privee
2. Connectez-vous : `membre1` / `Test1234!`
3. Allez sur `http://127.0.0.1:8000/utilisateurs/redirection/`
4. Vous etes redirige vers le **Dashboard Membre**

**Fonctionnalites disponibles :**
- Mon rang pour le cycle actif
- Solde de mes cotisations (cycle actif)
- Prochaines reunions (tours d'attribution)
- Statistiques (membres actifs, tontines, cycles, prets)
- Cotisations recentes
- Prets recents
- Remboursements recents

---

## 4. COMMENT CA MARCHE (TECHNIQUE)

### Systeme de roles
Le systeme utilise les **Groupes Django** :
- `President` : acces au dashboard admin
- `Tresorier` : acces au dashboard tresorier
- `Membre` : acces au dashboard membre

### Redirection automatique
Quand un utilisateur va sur `/utilisateurs/redirection/` :
```python
if user est dans groupe 'President':
    -> /utilisateurs/admin_dashboard/
elif user est dans groupe 'Tresorier':
    -> /utilisateurs/tresorier_dashboard/
else:
    -> /utilisateurs/user_dashboard/
```

### Protection des pages
Chaque dashboard verifie le groupe de l'utilisateur :
```python
if not request.user.groups.filter(name='President').exists():
    messages.error(request, "Vous n'avez pas l'autorisation...")
    return redirect('utilisateurs:redirection')
```

---

## 5. PROBLEMES FREQUENTS

### "Les anciens templates s'affichent"
1. **Vider le cache du navigateur** : `Ctrl+Shift+R` (ou `Cmd+Shift+R` sur Mac)
2. **Redemarrer le serveur** :
   ```bash
   # Arretez avec Ctrl+C puis relancez
   python manage.py runserver
   ```
3. **Supprimer les fichiers compiles** :
   ```bash
   find . -name "*.pyc" -delete
   find . -name "__pycache__" -type d -exec rm -rf {} +
   ```

### "Je vois seulement superutilisateur"
C'est normal ! Le superutilisateur n'a pas de groupe assigne. Il faut :
1. Creer des utilisateurs normaux (voir section 2)
2. Les assigner aux groupes President/Tresorier/Membre

### "NoReverseMatch" ou erreur URL
Les migrations n'ont peut-etre pas ete executees :
```bash
python manage.py migrate
```

### "Les groupes n'existent pas"
```bash
python manage.py migrate
```
Ou creez-les manuellement dans Django Admin > Groupes

---

## 6. RESUME EN 1 MINUTE

```bash
# Terminal 1 : Lancer l'app
python manage.py migrate
python manage.py runserver

# Dans le navigateur :
# 1. http://127.0.0.1:8000/admin/ -> creer les utilisateurs
# 2. http://127.0.0.1:8000/utilisateurs/login/ -> se connecter
# 3. http://127.0.0.1:8000/utilisateurs/redirection/ -> aller au bon dashboard
```

**Comptes de test :**
| Role | Username | Password |
|------|----------|----------|
| President | `president` | `Test1234!` |
| Tresorier | `tresorier` | `Test1234!` |
| Membre | `membre1` | `Test1234!` |
