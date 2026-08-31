# Compte rendu — passe du 31/08/2026

Bonjour Constance,

## Résumé en une phrase
Purge de 18 fiches zombies expirées (bloquant validate.py), puis condensation de
10 fiches en dérive « journal d'enquête » vers un mode d'emploi visiteur (2 en
fenêtre live + 8 au-delà, prioritairement les plus imminentes), tout publié sur
main au fil de l'eau, 0 blocker, healthcheck OK.

## 1. Démarrage
`precheck.sh` : arbre propre, verrou posé. `validate.py` initial : 431 événements,
**18 blockers** — zombies non purgés, toutes datées `d2=2026-07-31` (expirées depuis
plus de 30 jours, jamais purgées par la routine automatique). Corrigé en premier :
purge exécutée sur `index-full.html`, régénération (`split_i18n.py --apply`),
`validate.py` repasse à 0 blocker. Publié (431 → 413 événements).

## 2. Condensation `iv` (priorité de la passe)
Sélection sur le seuil WARN de `validate.py` (≥1200 caractères sur o/g/w), fenêtre
live d'abord : sur les 12 candidats de la fenêtre live, seuls 2 montraient une vraie
dérive d'enquêteur (« OUI, une voie existe, mais… », dates de vérification en clair,
étapes numérotées adressées au chercheur) — les 10 autres, déjà condensées lors de
passes précédentes, restent légitimement denses (contacts et tarifs réels
nombreux) et n'ont pas été retouchées, conformément à la leçon du 20-21/08 (« le
seuil de sélection redétecte le travail bien fait »).

Fiches condensées :
- **Fenêtre live** : Nikki Beach Miami Beach, Dubai Racing Carnival.
- **Au-delà, les plus imminentes** (cluster réouvertures d'hiver + Nouvel An,
  toutes en dérive nette) : Badrutt's Palace, Kulm Hotel St. Moritz, Airelles
  Courchevel, The Alpina Gstaad, Gstaad Palace, Gstaad New Year Music Festival,
  New Year's Eve Regatta (Saint-Barth), Formula 1 Etihad Airways Abu Dhabi Grand
  Prix (Paddock Club + Yasalam).

Une fiche examinée mais **non touchée** : Cheval Blanc Courchevel — son champ `w`
dépasse le seuil mais ne contient aucune marque de dérive (codes GDS, e-mails de
restaurants, prix), légitimement dense.

Méthode : lecture intégrale de chaque champ o/g/w, réécriture à la main en gardant
mot pour mot chaque fait dur (noms, fonctions, e-mails, téléphones, adresses, URL,
tarifs, horaires) et en jetant le raisonnement d'enquêteur, les « CORRECTION
IMPORTANTE », « ATTENTION, PIÈGE ÉCARTÉ », dates de vérification en préambule et
listes numérotées adressées au chercheur. Contrôle mécanique de non-perte de faits
(extraction e-mails/URL/téléphones/montants, avant vs après) sur les 10 fiches :
**4 pertes réelles détectées et corrigées avant publication** (une URL de
formulaire de contact et un numéro SIREN suisse sur Badrutt's Palace, l'URL de la
fiche-source du tarif Courchevel Tourisme sur Airelles, le tarif du standard
téléphonique Ticketcorner et la source `gstaad.ch` sur Gstaad New Year Music
Festival, un numéro de fax sur la fiche F1 Abu Dhabi) ; le reste des écarts
relevés étaient des faux positifs de format (espace différent, préfixe https://
absent). Au passage, deux champs de la fiche Gstaad Palace avaient perdu tous
leurs accents (probablement un défaut d'une passe antérieure) : corrigés en
réécrivant, sans changer aucun fait.

Compteurs `validate.py` avant/après condensation (sur l'état déjà purgé) :
iv.g 20 → 12 fiches au-dessus du seuil, iv.w 36 → 32.

## 3. Autres tâches
- Date de l'eyebrow mise à jour : 30 → 31 août 2026.
- `memoire.py changements` : rien à consigner (aucun commit d'index.html vieux de
  7 jours à comparer ce jour).
- Bandeau « Ouvertures & délais » : les 5 entrées actuelles sont toutes à échéance
  future (02/09 → 31/01/2027), aucune expirée à retirer, aucune nouvelle fenêtre
  datée découverte aujourd'hui.
- LOI DU SITE (recompte) : traductions 413/413 (0 manquante) ; séjours 371/413
  (reste 42) ; invitations 393/413 (reste 20). **Aucune des 11 fiches concernées
  n'est dans la fenêtre live stricte (auj.→+90j)** : ce sont les 8 ancres
  printemps 2027 (TEFAF, Watches and Wonders, Salone del Mobile, Fuorisalone,
  Festival de Cannes 80e, GemGenève, Grand Prix de Monaco, Royal Ascot) plus 3
  fiches joaillerie (Diamant rose/Chantilly, Precious Coral/Hong Kong, Designing
  the Gilded Age/Met) — toutes au-delà de +90 jours, à traiter par le backfill
  séjour+invitation habituel aux prochaines passes.
  KPI accès mondain (iv) : 96 % (269/278, fenêtre live).

## 4. Ce qui n'a pas été fait / signalé sans agir
- Branding de saison : « Été » toujours affiché au 31/08. Proposition maintenue à
  Constance : passer à « Automne 2026 » — jamais renommé sans accord explicite.
- Il reste 12 fiches (iv.g) et 32 fiches (iv.w) au-dessus du seuil WARN de 1200
  caractères, dont probablement une partie légitimement dense (à trier lot par
  lot, comme aujourd'hui) — à poursuivre aux prochaines passes.
- Recherche de nouveaux événements non entamée aujourd'hui : la priorité de purge
  (18 blockers) puis de condensation (10 fiches) a occupé la passe entière.
- Fiche 408 « Precious Coral » (L'École des Arts Joailliers, Hong Kong), signalée
  le 29/08 comme mal vérifiée par un contrôleur ayant cherché sur le mauvais
  sous-site (hub global au lieu de `/hk/en/`) : toujours sans séjour ni invitation
  complets, reste au backlog.
- 42 séjours et 20 invitations restent à compléter (LOI DU SITE), tous au-delà de
  +90 jours (voir §3) — sans urgence immédiate pour la fenêtre live, mais à
  traiter avant que ces événements n'entrent dans la fenêtre.

## 5. Publication et contrôles
Trois commits publiés au fil de l'eau (purge des zombies, condensation des 10
fiches, date eyebrow) via `.radar/session/publier.sh`. `validate.py` final :
0 blocker, 3 warnings (iv.g, iv.w résiduels + branding saison).
`healthcheck.sh` : OK (http=200, 413/413 événements, date fraîche).

## 6. Analyse des visites
Non consultée cette passe (GoatCounter non interrogé, la priorité est allée à la
purge et à la condensation) — à reprendre à la prochaine passe.

## 7. Anomalie initialement soupçonnée, puis écartée après vérification
En trouvant 18 blockers « zombie non purgé (d2=2026-07-31) » au démarrage,
j'ai d'abord soupçonné une panne du plancher quotidien (`passe-quotidienne.yml`,
qui tourne pourtant « avec succès » chaque jour d'après l'historique GitHub
Actions). **Vérification faite, ce n'est pas une anomalie** : le calcul du
seuil de purge (`d2 < aujourd'hui - 30 jours`) place le franchissement du seuil
exactement au 31/08/2026 pour un `d2` du 31/07/2026 (31/07 + 30 jours = 30/08 ;
la veille, 30/08, `d2` était encore égal à la limite, donc pas strictement
inférieur, donc pas encore purgé). Ces 18 fiches sont devenues zombies
aujourd'hui même, pas avant — le plancher automatique de ce matin (8h40 Paris)
les aurait purgées lui aussi, à quelques heures près. Rien à corriger côté
workflow ; je le note ici pour éviter qu'une future passe reparte du même
faux soupçon sans le vérifier par le calcul.
