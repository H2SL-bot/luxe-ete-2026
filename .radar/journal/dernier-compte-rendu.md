# Compte rendu — passe du 28/08/2026 (routine cloud, radar-routine-claude)

## Ce qui a été fait, dans l'ordre

### 1. Purge (précheck bloquait au démarrage)
`validate.py` bloquait sur 1 fiche zombie (`d2=2026-07-28`, au-delà du plancher
de 30 jours) : « Soldes d'été 2026 à Paris (prolongés jusqu'au 28 juillet) ».
Purgée avant tout le reste (436 → 435 fiches). Les 13 pages générées associées
(FR + 12 langues) ont été supprimées avec elle par `gen_pages.py`.

### 2. Condensation `iv` (priorité de la passe, doctrine)
**20 fiches condensées**, sélectionnées au seuil WARN de `validate.py`
(≥1200 caractères sur `iv.o`/`iv.g`/`iv.w`), les plus imminentes de la fenêtre
live en tête (25/04 → 01/07, dont deux guides POINT D'ENTRÉE à date
conventionnelle) : Villa Carmignac, Biennale Arte 2026, Dolce & Gabbana Beach
Club (Gurney's Montauk), Yves Saint Laurent and Photography (ICP), POINT
D'ENTRÉE Ventes aux enchères, POINT D'ENTRÉE Ventes presse et privées mode,
Villa Louis Vuitton/White 1921, Exposition On aura tout vu : Icônes (Sofitel),
Chanel boutique estivale (villa La Mistralée), Tisser broder sublimer (Palais
Galliera), Dior Saint-Tropez, Armani/Silos, Grand Hôtel de Cala Rossa, Hôtel &
Spa des Pêcheurs (Cavallo), Soirées d'été Casino Barrière Le Touquet, Clubs
privés Mayfair (Annabel's/5 Hertford Street/Oswald's), DaV Mare/Splendido Mare
(Belmond), Sottovento Club Porto Cervo, David Guetta Ushuaia Ibiza, Lio Ibiza.

Méthode : un agent par fiche (20 en parallèle, deux lots de 10), consigne
stricte (garder tout fait dur — nom, fonction, e-mail, téléphone, adresse,
URL entière, tarif, horaire —, jeter le journal d'enquête, viser 400 car./champ
sans jamais sacrifier un fait, ne jamais republier une donnée que la fiche
source signale elle-même comme réfutée/périmée/invalide). Contrôle mécanique
`verif_faits.py` ensuite : **4 alertes sur 20**, toutes examinées une à une
et confirmées légitimes après lecture du texte source — aucune vraie perte :
- fiche White 1921 : les deux prix (200 €/185 €) explicitement signalés
  contradictoires par la fiche elle-même (« PRIX : NE RIEN AFFICHER ») ;
- fiche Palais Galliera : l'URL de location d'espaces retirée avec le
  paragraphe « PRIVATISATION : À RETIRER EN L'ÉTAT » qui l'accompagnait
  (le lieu n'est pas dans la liste officielle des lieux privatisables) ;
- fiche Sottovento : les deux e-mails explicitement signalés comme
  « adresses invalides » par la fiche source ;
- fiche David Guetta/Ushuaia : les deux URL de presse en 404 documenté et
  l'adresse `jobs@` (hors sujet presse), plus des tarifs tiers contradictoires
  explicitement écartés par la fiche (« aucun n'est repris ici »).

WARN `validate.py` : `iv.g` 42→33 fiches au-dessus du seuil, `iv.w` 64→58
(excédent total en baisse d'environ 17 500 caractères). **39 fiches restent
au-dessus du seuil dans la fenêtre live** (contre 47 avant cette passe) — à
poursuivre par lots de 15-20 aux prochaines passes.

### 3. Entretien
- Date de l'eyebrow mise à jour : « vérifié le 28 août 2026 ».
- Bandeau « Ouvertures & délais » : les 5 entrées existantes (Boucheron,
  L'École des Arts Joailliers, Journées Particulières LVMH, Grand Prix de
  Monaco 2027, Royal Ascot 2027) ont toutes une échéance future — rien à
  retirer, rien de nouveau ajouté faute de temps disponible dans cette passe.
- `memoire.py changements` : rien à consigner (pas de commit d'index.html
  assez ancien disponible pour comparaison dans cette session).
- Relevé de visites du jour effectué (`relever_visites.py`).

## KPI (fenêtre live, aujourd'hui → +90 jours)

- **435 événements** en ligne (436 → 435 après purge du zombie).
- Traductions : **435/435 (100 %)** au global.
- Séjours (`sej`) : 74 manquants au global, **24 dans la fenêtre live**.
- Invitations (`iv`) : 34 manquantes au global, **24 dans la fenêtre live**.
- KPI accès mondain (`iv` sur fiches mondaines) : 275/297 (92 %).
- Dérive « journal d'enquête » (`iv.g`/`iv.w` ≥1200 car.) : **39 fiches dans
  la fenêtre live** (47 avant cette passe), 91 au global.

Ni séjours ni invitations manquants n'ont été retravaillés aujourd'hui : la
priorité de la passe, fixée par la doctrine, était la condensation.

## Publication

1 lot publié au fil de l'eau (purge + condensation), validé (`validate.py` :
0 bloqueur, 3 warnings non bloquants), poussé **directement sur `main`**
(aucun repli sur branche `claude/*` nécessaire). `healthcheck.sh` : http=200,
date fraîche, 435/435 événements en ligne, cohérent. `perfcheck.py` : 0
régression (poids -0,01 Mo, -1 événement, +0 séjour vs dernier point,
cohérent avec la purge).

## Analyse des visites

Compteur GoatCounter cumulé : 2 299 aujourd'hui contre 2 217 hier (+82) —
net rebond après le ralentissement du 27/08 (+11 seulement). Pas d'accès à
la répartition détaillée par pays/source dans cette session ; pas de chiffre
inventé sur ce point.

## Ce qui n'a pas pu être vérifié / reste ouvert

- **39 fiches** restent avec `iv.g`/`iv.w` en dérive « journal d'enquête »
  (≥1200 caractères) dans la fenêtre live — condensation à poursuivre par
  lots de 15-20 aux prochaines passes.
- **24 séjours et 24 invitations manquants** dans la fenêtre live — non
  traités aujourd'hui (priorité condensation).
- Branding « Été » toujours affiché (WARN non bloquant, connu depuis le
  25/08) — décision de rafraîchissement « Automne » à proposer à
  Constance/Gérald, non tranchée par une routine automatique.
- Les doutes ouverts dans `a-reverifier.md` (JustMe Porto Cervo, Soirées
  Barrière Deauville, doublon Été impérial Hôtel du Palais/Été Hôtel du
  Palais Biarritz) n'ont pas été rouverts aujourd'hui — non prioritaires
  devant la condensation.
- Recherche de nouveaux événements (couverture mondiale, joaillerie, guides
  d'accès) non entamée aujourd'hui : la priorité de doctrine était la
  condensation `iv`, qui n'est pas encore résorbée.
