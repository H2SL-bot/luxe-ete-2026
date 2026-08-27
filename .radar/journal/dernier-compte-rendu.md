# Compte rendu — passe du 27/08/2026 (routine cloud, radar-routine-claude)

## Ce qui a été fait, dans l'ordre

### 1. Purge (précheck bloquait au démarrage)
`validate.py` bloquait sur 1 fiche zombie (`d2=2026-07-27`, au-delà du plancher
de 30 jours) : « Notti Toscane 2026, gala Andrea Bocelli (Alpemare & Villa
Alpebella) ». Purgée avant tout le reste (437 → 436 fiches).

### 2. Condensation `iv` (priorité de la passe, doctrine)
**18 fiches condensées**, les plus imminentes de la fenêtre live (25/04 →
01/07 pour les événements, plus 5 guides « POINT D'ENTRÉE » à date
conventionnelle), sélectionnées au seuil WARN de `validate.py` (≥1200
caractères sur `iv.o`/`iv.g`/`iv.w`) : Villa Carmignac, Biennale Arte 2026,
Fondation Maeght (Peter Knapp), Loewe pop-up Saint-Tropez, Exposition Van
Cleef & Arpels, Into the Ocean (ArtScience x OceanX), Exposition Daniel Brush,
Dolce & Gabbana Beach Club (Gurney's Montauk), Yves Saint Laurent and
Photography (ICP), Beach takeover Luisa Spagnoli (Capri), Givenchy pop-up rue
Gambetta, WE ARE [still] HERE (Petit Palais), Ellsworth Kelly (Fondation
Maeght), et les guides POINT D'ENTRÉE Clienteling/VIC, Concierges Clefs d'Or,
Silencio, Lieux-scènes (Costes/Club 55/Caves du Roy/VIP Room), Billetteries
VIP sport de luxe.

Méthode : un agent par fiche (18 en parallèle), consigne stricte (garder tout
fait dur, jeter le journal d'enquête, viser 400 car./champ sans sacrifier un
fait, ne jamais republier une donnée que la fiche source signale elle-même
comme réfutée/périmée). Contrôle mécanique `verif_faits.py` ensuite :
9 alertes au premier passage, **4 vraies pertes** (une URL de connexion presse
raccourcie en mot-clé au lieu de rester une URL, un e-mail secondaire de
service oublié, deux URL sources sur une fiche Fondation Maeght) — corrigées
manuellement. Les 5 alertes restantes ont été examinées une à une et confirmées
légitimes : deux étaient des pistes mortes explicitement décrites comme telles
par le texte source (page « communication » sans rapport, échéances de
politique d'annulation héritées d'une édition passée et explicitement
signalées comme non applicables), les trois autres étaient des montants
rumeur/tiers explicitement réfutés par la fiche elle-même (table Caves du Roy
3000-15000 €, champagne 400 €, tarif Sodexo Eiffel Jumping 2026 explicitement
qualifié de périmé). Aucune de ces cinq n'a donc été réinjectée.

WARN `validate.py` : `iv.g` 53→42 fiches au-dessus du seuil, `iv.w` 75→64
(excédent total en baisse de ~43 000 caractères). **47 fiches restent
au-dessus du seuil dans la fenêtre live** (69 au global, y compris les fiches
déjà passées conservées 30 jours) — à poursuivre par lots de 15-20 aux
prochaines passes, en commençant par les plus imminentes.

### 3. Entretien
- Date de l'eyebrow mise à jour : « vérifié le 27 août 2026 ».
- Bandeau « Ouvertures & délais » : les 5 entrées existantes (Boucheron,
  L'École des Arts Joailliers, Journées Particulières LVMH, Grand Prix de
  Monaco 2027, Royal Ascot 2027) ont toutes une échéance future — rien à
  retirer aujourd'hui, rien de nouveau identifié à ajouter dans le temps
  disponible de cette passe.
- `memoire.py changements` : rien à consigner (pas de commit d'index.html
  assez ancien à comparer dans l'historique disponible de cette session).

## KPI (fenêtre live, aujourd'hui → +90 jours)

- **436 événements** en ligne (437 → 436 après purge du zombie).
- Traductions : **436/436 (100 %)**.
- Séjours (`sej`) : 75 manquants au global, **30 dans la fenêtre live**.
- Invitations (`iv`) : 34 manquantes au global, **24 dans la fenêtre live**.
- KPI accès mondain (`iv` sur fiches mondaines) : 276/298 (92 %).

Ni séjours ni invitations n'ont été retravaillés aujourd'hui : la priorité de
la passe, fixée par la doctrine, était la condensation — à reprendre dès la
prochaine passe si la fenêtre live des dérives `iv` se réduit encore.

## Publication

1 lot publié au fil de l'eau (purge + condensation), validé (`validate.py` :
0 bloqueur), poussé directement sur `main` (aucun repli sur branche `claude/*`
nécessaire — le push direct a été accepté dès le début de passe).
`healthcheck.sh` : http=200, date fraîche, 436/436 événements en ligne,
cohérent. `perfcheck.py` : 0 régression (poids -0,01 Mo, -1 événement, -1
séjour vs dernier point, cohérent avec la purge).

## Analyse des visites

Compteur GoatCounter cumulé : 2 217 aujourd'hui contre 2 206 hier (+11).
La progression s'est nettement ralentie par rapport aux jours précédents
(2 153 → 2 206 → 2 217, soit +53 puis +11) — à surveiller, sans tirer de
conclusion hâtive sur un seul jour. Pas d'accès à la répartition par pays/
source dans cette session (tableau de bord détaillé non interrogé) : pas de
chiffre inventé sur ce point.

## Ce qui n'a pas pu être vérifié / reste ouvert

- **47 fiches** restent avec `iv.g`/`iv.w` en dérive « journal d'enquête »
  (≥1200 caractères) dans la fenêtre live — condensation à poursuivre par
  lots de 15-20 aux prochaines passes.
- **30 séjours et 24 invitations manquants** dans la fenêtre live — non
  traités aujourd'hui (priorité condensation), à reprendre dès que la
  dérive `iv` sera résorbée ou en alternance.
- Branding « Été » toujours affiché (WARN non bloquant, connu depuis le
  25/08) — à proposer à Gérald/Constance pour le rafraîchissement « Automne ».
- Les doutes ouverts consignés dans `a-reverifier.md` lors des passes
  précédentes (JustMe Porto Cervo, Soirées Barrière Deauville, doublon Été
  impérial Hôtel du Palais/Été Hôtel du Palais Biarritz) n'ont pas été
  rouverts aujourd'hui — non prioritaires devant la condensation, toujours en
  attente.
- Artifact Claude de la doctrine (`89b85688-ff57-481d-82d7-f7792051b066`) :
  non retesté aujourd'hui (échec connu et documenté depuis le 21/08) ; sans
  conséquence pour le public, constanceparis7.com étant la seule adresse qui
  compte et étant à jour.

## Erreurs rencontrées

Aucune erreur d'outil bloquante. Le contrôle mécanique `verif_faits.py` a
fonctionné comme prévu : 9 alertes initiales, 4 vraies pertes corrigées, 5
confirmées légitimes après lecture individuelle du texte source — conforme à
la méthode déjà établie (leçons des 20/08, 21/08 et 25/08). Rien de nouveau à
ajouter à `lessons.md` cette fois : la procédure existante a suffi.
