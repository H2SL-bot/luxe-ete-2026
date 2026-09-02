# Compte rendu — passe du 02/09/2026

Bonjour Constance,

## Résumé en une phrase
Purge de 3 fiches zombies, condensation de 8 fiches en dérive « journal d'enquête »,
découverte et fusion de 2 doublons exacts/quasi exacts trouvés au passage (Calder,
Monte-Carlo Summer Festival), retrait de 3 lignes personnelles (mobile/directe)
publiées à tort en violation de la règle du 20/08 — tout publié sur main au fil de
l'eau, 0 blocker, healthcheck OK.

## 1. Démarrage
`precheck.sh` : arbre propre, verrou posé. `validate.py` initial : 405 événements,
**3 blockers** — zombies non purgées (d2=2026-08-02, Polo Exhibition Week & Practices,
Jumping International de Dinard, Concerts au Palais Princier). Purgées en premier,
publiées (405 → 402 événements).

## 2. Condensation `iv` (priorité de la passe)
Sélection sur le seuil WARN de `validate.py` (≥1200 caractères sur o/g/w). Sur les
27 candidats détectés, la grande majorité (Villa Carmignac, Biennale Arte, POINT
D'ENTRÉE, Armani/Silos, Grand Hôtel de Cala Rossa, Dubai Racing Carnival, Saint-Barth
Cata Cup, F1 Abu Dhabi, Gstaad New Year Music Festival, etc.) sont légitimement denses
— grilles tarifaires, horaires, contacts réels — et n'ont pas été retouchées, conforme
à la leçon du 20-21/08 (« le seuil de sélection redétecte le travail bien fait »).

**8 fiches réellement en dérive, condensées** (lecture intégrale, faits durs
recopiés à l'identique, raisonnement d'enquêteur jeté) :
- BALLET - The Making of an Etoile (Alliance Française Singapour)
- LINDER: Goddess of the Mind (Chanel Nexus Hall, Tokyo)
- Monte-Carlo Sporting Summer Festival 2026 (après fusion, voir §3)
- Polo, Côte d'Azur Cup
- Bow Wow Meow Ball 2026 (ARF Hamptons)
- Cowes Week 2026 (Bicentenaire)
- SantAnna Mykonos, Nuits headline
- Calder. Rêver en équilibre (après fusion, voir §3)

Compteurs `validate.py` iv.g/iv.w avant/après (sur l'état déjà purgé) :
iv.g 10 → 3 fiches au-dessus du seuil (excédent 9373 → 3084 car.),
iv.w 26 → 18 fiches (excédent 18491 → 8540 car.).

## 3. Découverte en chemin : deux doublons exacts/quasi exacts
En condensant, deux paires de fiches sur le MÊME événement sont apparues :
- **« Calder. Rêver en équilibre »** existait en double (même lieu, mêmes dates
  15/04-16/08, deux créations à des passes différentes) — fusionnées en une seule
  fiche, tous les faits distincts des deux versions conservés (dont les contacts
  internationaux Meagan Jones/Isabella Capece Galeota).
- **« Monte-Carlo Summer Festival »** existait en double (même URL officielle, même
  source, même lieu — une fiche pour tout le festival, une pour le seul volet
  dîners-spectacles d'août) — fusionnées, tous les contacts presse nommés (Bourgeat,
  Cristin, Esteve, Burg, Dominici) et tarifs conservés.
Déclarées dans `.radar/renommages.json` avec motif complet, pour que le filet
anti-perte de données ne les prenne pas pour une suppression.

## 4. Découverte en chemin : coordonnées nominatives republiées à tort
En relisant ces fiches, plusieurs contenaient des **lignes personnelles explicitement
qualifiées de « directe » ou « portable »**, en violation de la règle du 20/08/2026 —
probablement réintroduites par des passes de composition postérieures à cette date :
- Monte-Carlo (x2, fusionnées) : 4 « lignes fixes directes, publiées » nominatives
  (Bourgeat, Cristin, Dominici, Esteve) et leurs e-mails `prenom.nom@sbm.mc` — retirés,
  noms et fonctions conservés, repli sur `presse@sbm.mc` (boîte de service).
- Cowes Week 2026 : un numéro tenu par Grace Murray (format mobile UK, `iv.c`) — retiré.
- Sommets Musicaux de Gstaad 2027 : le « portable direct » d'Alexandra Egli
  (+41 79 293 84 10) — retiré de `iv.o` et de `iv.c`, repli sur l'agence Music Planet.

**Signalement pour la suite** : j'ai testé `contacts_nettoyer.py --blanc` (l'outil
prévu pour ce nettoyage à l'échelle du site) et il propose de retirer 39 coordonnées
sur 20 fiches — mais une lecture des candidats montre un **taux de faux positifs
significatif** : des standards explicitement écrits « standard », « ligne fixe, non
nominative » ou des boîtes de billetterie (`ticket@grimaldiforum.com`,
`ticketsales@dubairacingclub.com`) sont retirés à tort dès qu'un nom de personne
apparaît dans le même segment de texte, et une entrée `{"t":"nom"}` portant une
raison sociale (SIRET Twiga Porto Cervo) est traitée comme une coordonnée
personnelle. **Ne pas lancer `--appliquer` en l'état** : le classifieur de
`RE_MOBILE_FR`/`LIGNE_DIRECTE` doit apprendre à exempter un numéro explicitement
qualifié de « standard »/« non nominatif » dans son propre libellé avant d'être fiable
à l'échelle du site. J'ai traité les cas identifiés manuellement (voir ci-dessus) et
consigné la leçon dans `lessons.md`.

## 5. Autres tâches
- Date de l'eyebrow mise à jour : 1er → 2 septembre 2026.
- `memoire.py changements` : rien à consigner (aucun commit d'index.html vieux de
  7 jours à comparer ce jour).
- Bandeau « Ouvertures & délais » : 5 entrées, toutes à échéance future ou du jour
  même (02/09 → 31/01/2027), rien à retirer.
- **Rendez-vous de mémoire manqué de peu** : la doctrine fixe au 2 septembre 2026
  10h l'ouverture des réservations Boucheron (place Vendôme), premier rendez-vous de
  mesure pour `.radar/memoire.ndjson` (« consigner l'heure d'épuisement réelle »).
  Cette passe s'exécute à 6h15 Paris, avant l'ouverture : impossible de constater
  l'épuisement aujourd'hui. À vérifier lors d'une prochaine connexion dans la
  journée ou à la passe de demain (la fenêtre de vente reste identifiable via le
  bandeau, `data-exp="2026-09-02"`).
- LOI DU SITE (recompte, sur 400 fiches) : traductions 400/400 (0 manquante) ;
  séjours 372/400 (reste 28, dont **2 seulement en fenêtre live** — les deux fiches
  joaillerie Diamant rose/Chantilly et Designing the Gilded Age/Met, d1 respectivement
  17/10 et 22/10/2026) ; invitations 384/400 (reste 16, mêmes 2 en fenêtre live).
  KPI accès mondain (iv) : 97 % (262/270, fenêtre live).
  Ces 2 fiches restent au backlog joaillerie pour une prochaine passe (recherche +
  vérification adversariale, hors priorité de condensation du jour).

## 6. Ce qui n'a pas été fait / signalé sans agir
- Branding de saison : « Été » toujours affiché au 02/09. Proposition maintenue à
  Constance : passer à « Automne 2026 » — jamais renommé sans accord explicite.
- Il reste 3 fiches (iv.g) et 18 fiches (iv.w) au-dessus du seuil WARN de 1200
  caractères, toutes vérifiées une par une aujourd'hui et jugées légitimement denses
  (aucune dérive « journal d'enquête » détectée) — sauf « Sommets Musicaux de
  Gstaad 2027 » et « The I.C.E. St. Moritz », partiellement denses avec une mise en
  forme d'enquêteur (listes numérotées, gras, verdicts « OUI »/« NON ») mais sans
  perte de valeur informative : à trancher lot par lot à une prochaine passe si le
  format continue de gêner la lecture.
- Recherche de nouveaux événements non entamée : la priorité de purge, condensation,
  fusion des doublons et nettoyage des coordonnées personnelles a occupé la passe
  entière — conforme à la consigne (« PRIORITAIRE sur la recherche de nouveaux
  événements »).
- `contacts_nettoyer.py --appliquer` non lancé (voir §4) : la correction de son
  taux de faux positifs est laissée en tâche pour une prochaine passe ou pour
  Constance/Gérald.

## 7. Publication et contrôles
Cinq commits publiés au fil de l'eau via `.radar/session/publier.sh` (purge zombies ;
condensation + fusion des doublons ; retrait ligne mobile Gstaad ; date eyebrow).
`validate.py` final : 0 blocker, 3 warnings (iv.g/iv.w résiduels légitimes + branding
saison). `healthcheck.sh` : OK (http=200, 400/400 événements, date fraîche).

## 8. Analyse des visites
Compteur GoatCounter (cumulatif) : 2 449 ce matin contre 2 427 hier — progression
régulière d'une vingtaine de visites/jour, dans la continuité de la semaine (2206 →
2449 du 26/08 au 02/09). Rien d'anormal à signaler ; pas de rupture de tendance.
Répartition pays/sources non consultée en détail cette passe (priorité donnée au
nettoyage) — à reprendre à la prochaine passe.
