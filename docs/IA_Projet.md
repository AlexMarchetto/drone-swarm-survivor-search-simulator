IA Projet

# Contexte et exemples

Scénarios nécessitant la résolution d’une tache de façon distribuée par des agentes autonomes et qui requiert de la simulation

Ex :

- Essaim de drones dans une zone à risque

- Mobilité urbaine

- Propagation de fake news

- Inondations

- Epidémie

- Gestion hospitalière en cas d’épidémie

- Etc …

# Etape

- Modélisation du problème

  - Agents

  - Environnement

  - Système de communication

  - Règles

- Simulation

- Évaluation (comportement émergent)

# Evaluation

Préparer une présentation de 15 minutes expliquant :

- Modèle proposé

- Evolution des paramètres simulés

- Résultats obtenus

- Taux de réussite selon les scénarios (comportement émergent)

- Choix d’implémentation (une interface graphique est un plus mais pas obligatoire)

- Difficultés rencontrées

# Ce qu’il faut faire

- Effectuer une recherche dans la littérature

- Définir un scénario

- Valider le scenario avec l’enseignante

# Idée de sujet : Un essaim de drones pour retrouver des personnes après une catastrophe

Article de référence : [*Search and rescue with autonomous flying robots through behavior-based cooperative intelligence*](https://link.springer.com/article/10.1186/s41018-018-0045-4)

Scénario :

En l’an 2077, une catastrophe naturelle a failli décimer la planète bleue, la Terre. Une pluie de météorites d’un niveau sans précédent a eu lieu.

Presque plus de la moitié de la population mondiale a péri. Les météorites en s’écrasant, ont libéré une poussière extraterrestre toxique qui se propage avec le vent. Les villes sont toutes en ruines et les réseaux de communication sont détruits. Des zones de survie sont déployé pour accueillir les survivants car les villes ne sont plus habitables.

Pas très loin de Grenoble, une zone de survie a été créé. Les chercheurs présents à l’intérieur travaillent jour et nuit pour détecter les survivants potentielles.

10 survivants sont détectés à Grenoble, mais compliqué de les retrouver dans toutes ces ruines et aucun moyen de détecter directement leurs position. De plus, une tempête approche et risque de recouvrir toute la ville de poussière toxique.

Une seule solution, déployer 5 drones autonomes pour les localiser avant la tempête. Chaque drone choisit son chemin, possède une batterie limitée et partage ses découvertes avec les drones proches.

L’objectif (de la simulation) : observer si le partage d’information permet aux drones de retrouver davantage de survivants avant la fin du temps disponible.

## Simulation :

Les distances peuvent être mesurées en **cases.**

Caractéristiques des drones :

- **Autonomie de la batterie :** énergie dont le drone dispose. (ex : un déplacement d’une case consomme une barre d’énergie)

  - 28 minutes de vol

    - Tableau 2, page 11 de l’article

- **Portée de détection :** distance à laquelle le drone peut repérer une personne.

  - Détecte les personnes dans un rayon de 15 mètres.

    - *Tableau 3, page 12 de l’article*

- **Portée de communication :** distance maximale pour échanger des informations avec un autre drone.

  - Le dispositif Wi-Fi possède une portée de 805 mètres.

    - *Tableau 3, page 12 de l’article*

- **Vitesse :** nombre de cases que le drone peut parcourir par tour.

  - La vitesse horizontale maximale est de 20 m/s

    - *Tableau 2, page 11 de l’article*

- **Communication activée :** possibilité de partager les zones explorées et les personnes trouvées.

  - Les drones communiquent par Wi-Fi. Les équipements peuvent être activés ou désactivés dans le simulateur.

    - *Section « Sensors and equipments » de l’article*

  - *Dans l’article, la communication est toujours activée.*

- Nombre de drones

**Environnement :** Une grille de 30 x 30 cases (on peut commencer avec 10 x 10 case) représentant Grenoble, avec une base, des zones interdites au vol et 10 survivants immobiles.

**Règle des drones** : Explorer les zones encore inconnues, éviter les obstacles et les collisions, puis revenir à la base avant d’épuiser la batterie. Chaque drone décide à partir de ses informations locales.

**Détection** : Une personne est automatiquement repérée lorsqu’elle entre dans la portée de détection du drone.

**Communication** : A chaque tour, les drones à portée échangent les cases explorées et les positions des personnes trouvées.

## Simulation 1 :

| Élément  | Valeur choisie    |
|----------|-------------------|
| Une case | 5 mètres de côté  |
| Un tour  | 1 seconde simulée |
| Carte    | 30 x 30 cases     |

La carte représente un secteur de Grenoble de 150 x 150 mètres.

Dans ce cas, un portée de détection de 15 mètres correspond à un rayon de 3 cases.

Au niveau de la communication entre les drones, 3 configurations sont possibles :

| Configuration         | Portée                     | Origine                               |
|-----------------------|----------------------------|---------------------------------------|
| Sans communication    | Aucun échange              | Comparaison ajoutée dans notre projet |
| Communication locale  | 25 mètres, soit 5 cases    | Adaptation choisie pour notre carte   |
| Communication étendue | 805 mètres, soit 161 cases | Valeur de référence de l’article      |

Pour commencer, on utilise la communication locale à 5 cases. Deux drones peuvent échanger lorsque leur distance en ligne droite est inférieure ou égale à cette portée.

A chaque tour, ils partagent :

- Les cases déjà explorées.

- Les positions des survivants repérés.

- Leur propre position.

Chaque drone conserve les informations reçues dans sa mémoire individuelle et choisit ensuite son déplacement. Il peut retransmettre ces informations lorsqu’il rencontre d’autres drones : les découvertes circulent progressivement dans le groupe.
