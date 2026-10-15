# Drone Swarm Survivor Search Simulator

Projet de simulation multi-agents mettant en scène un **essaim de drones autonomes chargé de rechercher des survivants dans une zone sinistrée**.

Le projet repose principalement sur **Mesa**, un framework Python de modélisation multi-agents, ainsi que **Solara** pour la visualisation et l'interface interactive de la simulation.

## Collaborateurs

- **Alex Marchetto**
- **Alexis Rebelo**

---

## Objectifs du projet

L'objectif du projet est de développer une simulation dans laquelle plusieurs drones coopèrent afin d'explorer un environnement et de localiser des survivants.

La simulation doit permettre d'étudier différents comportements liés aux **systèmes complexes** et aux **systèmes multi-agents**, notamment :

- la coordination entre plusieurs agents ;
- l'exploration distribuée d'un environnement ;
- la recherche de survivants ;
- la communication ou le partage d'informations entre drones ;
- l'évitement des zones déjà explorées ;
- l'optimisation de la couverture de la zone ;
- l'observation de comportements émergents à l'échelle de l'essaim.

Le projet pourra évoluer afin d'intégrer différentes stratégies de déplacement, contraintes ou méthodes de coordination.

---

# Technologies utilisées

Le projet est développé en **Python**.

Principales bibliothèques utilisées :

| Technologie | Utilisation |
|---|---|
| Python | Langage principal |
| Mesa | Simulation multi-agents |
| Solara | Interface et visualisation interactive |
| Pandas | Manipulation et analyse des données |
| Git | Gestion de versions |

Version de Mesa actuellement utilisée :

```text
Mesa 3.5.1
```

---

# Structure du projet

La structure du dépôt peut évoluer pendant le développement.

Une organisation typique du projet est la suivante :

```text
drone-swarm-survivor-search-simulator/
│
├── agents/                 # Définition des agents
│   └── ...
│
├── model/                  # Modèle principal de simulation
│   └── ...
│
├── visualization/          # Visualisation / interface Solara
│   └── ...
│
├── data/                   # Données éventuelles de simulation
│   └── ...
│
├── main.py                 # Point d'entrée éventuel du programme
│
├── requirements.txt        # Dépendances Python
│
├── README.md
│
└── .gitignore
```

> Cette arborescence est indicative et pourra être adaptée en fonction de l'évolution du projet.

---

# Installation

## 1. Cloner le dépôt

Avec Git :

```powershell
git clone <URL_DU_DEPOT>
```

Puis accéder au projet :

```powershell
cd drone-swarm-survivor-search-simulator
```

---

## 2. Créer un environnement virtuel Python

Il est recommandé d'utiliser un environnement virtuel afin d'isoler les dépendances du projet.

Sous Windows PowerShell :

```powershell
python -m venv .venv
```

---

## 3. Activer l'environnement virtuel

Sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Une fois activé, le terminal doit afficher quelque chose de similaire à :

```text
(.venv) PS C:\...\drone-swarm-survivor-search-simulator>
```

### Problème d'autorisation PowerShell

Si PowerShell refuse l'exécution du script d'activation, utiliser :

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Puis réessayer :

```powershell
.\.venv\Scripts\Activate.ps1
```

---

# Installation des dépendances

## Méthode recommandée

Si le projet contient un fichier `requirements.txt` :

```powershell
pip install -r requirements.txt
```

---

## Installation manuelle

Les principales dépendances peuvent également être installées manuellement :

```powershell
pip install mesa==3.5.1 solara pandas
```

---

## Vérifier l'installation

Pour vérifier que les dépendances principales sont correctement installées :

```powershell
python -c "import mesa, solara, pandas; print(mesa.__version__)"
```

La version actuellement utilisée dans le projet doit afficher :

```text
3.5.1
```

---

# Générer le fichier requirements.txt

Après installation ou ajout de nouvelles dépendances, il est possible de sauvegarder les versions utilisées :

```powershell
pip freeze > requirements.txt
```

Cela permet aux autres collaborateurs de reproduire le même environnement avec :

```powershell
pip install -r requirements.txt
```

---

# Exécution du projet

L'environnement virtuel doit être activé avant de lancer la simulation :

```powershell
.\.venv\Scripts\Activate.ps1
```

## Exécution Python

Si le point d'entrée du projet est `main.py` :

```powershell
python main.py
```

---

## Exécution avec Solara

Si l'interface Mesa/Solara se trouve par exemple dans un fichier `app.py` :

```powershell
solara run app.py
```

Solara démarre alors un serveur local.

L'adresse de l'application est généralement indiquée dans le terminal, par exemple :

```text
http://localhost:8765
```

Ouvrir cette adresse dans un navigateur afin d'accéder à la simulation.

> La commande exacte de lancement pourra être adaptée lorsque le point d'entrée définitif de l'application sera fixé.

---

# Arrêter la simulation

Dans le terminal :

```text
Ctrl + C
```

---

# Désactiver l'environnement virtuel

Lorsque le développement est terminé :

```powershell
deactivate
```

---

# Workflow de développement

Avant de commencer à travailler :

```powershell
git pull
```

Activer ensuite l'environnement :

```powershell
.\.venv\Scripts\Activate.ps1
```

Installer les éventuelles nouvelles dépendances :

```powershell
pip install -r requirements.txt
```

Après modification du projet :

```powershell
git status
```

Puis :

```powershell
git add .
```

Créer un commit :

```powershell
git commit -m "Description des modifications"
```

Et envoyer les modifications :

```powershell
git push
```

---

# Gestion des branches Git

Afin d'éviter de travailler directement sur la branche principale, il est possible de créer une branche pour chaque fonctionnalité.

Exemple :

```powershell
git checkout -b feature/drone-movement
```

Après les modifications :

```powershell
git add .
git commit -m "Ajout du déplacement des drones"
git push -u origin feature/drone-movement
```

Quelques exemples de noms de branches :

```text
feature/drone-movement
feature/survivor-detection
feature/map-generation
feature/drone-communication
feature/visualization
fix/collision
```

---

# Mise à jour des dépendances

Lorsqu'une nouvelle bibliothèque est ajoutée au projet :

```powershell
pip install nom_de_la_bibliotheque
```

Puis mettre à jour :

```powershell
pip freeze > requirements.txt
```

Le fichier `requirements.txt` doit ensuite être ajouté au prochain commit.

---

# Configuration Git recommandée

Le dossier `.venv` ne doit pas être envoyé sur Git.

Le fichier `.gitignore` devrait notamment contenir :

```gitignore
# Virtual environment
.venv/
venv/

# Python
__pycache__/
*.py[cod]
*.pyd

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Pytest
.pytest_cache/

# Environment variables
.env
```

---

# Concepts principaux

## Agent

Un agent représente une entité autonome de la simulation.

Dans notre cas, les principaux agents pourront être :

- des drones ;
- des survivants ;
- éventuellement des obstacles ou d'autres éléments dynamiques.

Chaque drone pourra disposer de son propre état et de ses propres règles de comportement.

---

## Modèle

Le modèle représente l'environnement global de la simulation.

Il est notamment responsable :

- de la création des agents ;
- de la gestion de l'environnement ;
- de l'évolution temporelle de la simulation ;
- de la collecte des statistiques ;
- de la gestion des conditions de début et de fin de simulation.

---

## Simulation multi-agents

Contrairement à un programme centralisé classique, chaque drone peut prendre des décisions en fonction :

- de son environnement local ;
- de ses connaissances ;
- des informations reçues d'autres agents ;
- des règles définies dans son comportement.

Des comportements complexes peuvent alors émerger à partir de règles individuelles relativement simples.

---

# Indicateurs possibles

Afin d'évaluer les performances des différentes stratégies, plusieurs métriques pourront être utilisées :

- nombre de survivants trouvés ;
- temps nécessaire pour trouver tous les survivants ;
- pourcentage de la carte explorée ;
- nombre de déplacements effectués ;
- zones explorées plusieurs fois ;
- distance parcourue par chaque drone ;
- nombre de communications entre drones ;
- efficacité globale de l'essaim.

Ces informations pourront notamment être enregistrées et analysées à l'aide de **Pandas** et des outils de collecte de données proposés par **Mesa**.

---

# Évolutions possibles

Plusieurs fonctionnalités pourront être ajoutées progressivement :

- génération aléatoire de cartes ;
- obstacles ;
- différents types de terrains ;
- batteries limitées pour les drones ;
- stations de recharge ;
- communication limitée en distance ;
- perte de communication ;
- partage d'une carte commune ;
- algorithmes de recherche différents ;
- comparaison entre stratégies ;
- intelligence collective ;
- apprentissage automatique ;
- optimisation de la répartition des drones ;
- apparition aléatoire de survivants ;
- interface permettant de modifier les paramètres de la simulation ;
- visualisation de statistiques en temps réel.

---

# Commandes utiles

Créer l'environnement :

```powershell
python -m venv .venv
```

Activer l'environnement :

```powershell
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
pip install -r requirements.txt
```

Vérifier Mesa :

```powershell
python -c "import mesa; print(mesa.__version__)"
```

Vérifier les principales bibliothèques :

```powershell
python -c "import mesa, solara, pandas; print(mesa.__version__)"
```

Sauvegarder les dépendances :

```powershell
pip freeze > requirements.txt
```

Lancer un programme Python :

```powershell
python main.py
```

Lancer une application Solara :

```powershell
solara run app.py
```

Désactiver l'environnement :

```powershell
deactivate
```

---

# État actuel

L'environnement Python a été configuré avec succès.

Mesa est correctement installé avec la version :

```text
3.5.1
```

Les imports suivants fonctionnent correctement :

```python
import mesa
import solara
import pandas
```

Le projet peut maintenant poursuivre l'implémentation du modèle multi-agents et de son interface de visualisation.

---

# Auteurs

**Alex Marchetto**  
**Alexis Rebelo**

Projet réalisé dans le cadre d'un travail sur l'**Intelligence Artificielle et les Systèmes Complexes**.