# Compte rendu — passe du 25/08/2026 (routine cloud, radar-routine-claude)

## Ce qui a été fait, dans l'ordre

### 1. Purge (précheck bloquait au démarrage)
`validate.py` bloquait sur 7 fiches zombies (`d2=2026-07-25`, gardées 30 jours,
au-delà du plancher) : Grandes Eaux Nocturnes de Versailles, Polo Hamptons
(Social Life Magazine), Nice Jazz Fest, Watermill Center Summer Benefit, King
George Weekend Ascot, MADE IN MYKONOS, Global Gift Gala Marbella. Purgées et
publiées en premier lot (452 → 445 fiches). C'était un blocage bloquant toute
publication ultérieure — traité avant tout le reste.

### 2. Condensation `iv` (priorité de la passe, doctrine)
**18 fiches condensées**, les plus imminentes de la fenêtre live (29/08 →
12/09), sélectionnées au seuil WARN de `validate.py` (≥1200 caractères sur
`iv.o`/`iv.g`/`iv.w`) : Twiga Porto Cervo, Hamptons Polo, Meeting de Deauville,
D&G x Casa Amor, Principote, La Co(o)rniche, La Gritta, JustMe Porto Cervo,
Bagni Fiore/Langosteria, Été impérial Hôtel du Palais, Soldes Milan, Jesus
Christ Superstar Singapour, Grand Palais d'été, Grimaldi Forum Monaco &
l'Automobile, Été Hôtel du Palais Biarritz, Journey Within Hermès, Phi Beach,
Maxi Yacht Rolex Cup.

Méthode : un agent par fiche (18 en parallèle), consigne stricte (garder tout
fait dur, jeter le journal d'enquête, viser 400 car./champ sans sacrifier un
fait). Contrôle mécanique `verif_faits.py` ensuite : 7 alertes, dont 4 étaient
des suppressions légitimes (tarif tiers réfuté, page presse vide, horodatage
machine confondu avec un téléphone) et **3 étaient de vraies pertes** (URL
secondaires abrégées ou omises malgré la consigne) — corrigées manuellement
avant publication. Leçon consignée dans `lessons.md`.

WARN `validate.py` : iv.g 77→66 fiches, iv.w 104→88 fiches (excédent total en
baisse de ~90 000 caractères). **62 fiches restent au-dessus du seuil dans la
fenêtre live** (44 après ce lot) — à poursuivre par lots de 15-20 aux
prochaines passes.

### 3. Le piège du « 31 août » (14 fiches restantes au 22/08, échéance ferme avant le 1er septembre)
Recherche à la source officielle pour les 12 fiches réelles restantes (les 2
« Conseil » sont intentionnellement bornées à août, non touchées) :

**2 doutes tranchés** : La Gritta (Portofino) et Le Westminster/Le Pavillon
(Touquet) sont des établissements ouverts À L'ANNÉE, pas des pop-up saisonniers
— d2 porté à 2027-12-31 (convention déjà en usage sur le site pour les lieux
permanents, ex. « POINT D'ENTRÉE, Les lieux-scènes ouverts à la réservation »).

**1 erreur du 22/08 corrigée** : « Milan en mode Ferragosto » avait été laissée
au 31/08 sur la foi d'une hypothèse jamais vérifiée (« sujet intrinsèquement
borné à la mi-août »). Les sources CITÉES PAR LA FICHE ELLE-MÊME (Fondazione
Prada, Armani/Silos) courent en réalité jusqu'à fin septembre / fin octobre /
20 décembre 2026. d2 porté à 2026-12-31.

**9 dates étendues avec preuve partielle ou estimation documentée**, toutes
consignées en détail dans `a-reverifier.md` avec leur source et leur niveau de
confiance : Terrasses palaces parisiens → 04/10 (Crillon confirmé
officiellement, seule date ferme sur 5 palaces), La Co(o)rniche → 30/09
(programmation DJ de septembre confirmée à la source, jour exact non publié),
Dioriviera Cannes → 15/09 (précédent 2024, non confirmé 2026), Bagni
Fiore/Langosteria → 30/09 (source secondaire), Chanel East Hampton → 30/09
(buffer, aucune date trouvée), Principote → 30/09 (plage « mai-octobre » d'une
source secondaire), Été impérial Hôtel du Palais → 07/09 (aligné sur la fiche
sœur du même palace, probable doublon à vérifier), JustMe Porto Cervo → 07/09
(signal inquiétant : billetterie officielle Xceed ne liste plus rien après le
24/08 — **à recontrôler en priorité**), Soirées Barrière Deauville → 15/09
(l'existence même de cette fiche sous ce nom est mise en doute : aucune source
officielle ne mentionne des « soirées d'été » Barrière à Deauville — à
requalifier ou retirer à la prochaine passe).

**Résultat : 0 fiche réelle restante au 31/08** (hors les 2 « Conseil »
volontaires). Le bouchon ne fera plus disparaître d'événement réel le
1er septembre.

## KPI (fenêtre live, aujourd'hui → +90 jours)

- **445 événements** en ligne (452 → 445 après purge).
- Traductions : **445/445 (100 %)**.
- Séjours (`sej`) : 82 manquants au global, **14 dans la fenêtre live** — tous
  des fiches joaillerie (Journées du Patrimoine, ventes Sotheby's/Phillips/
  Christie's Genève, expositions internationales). À traiter en priorité à la
  prochaine passe.
- Invitations (`iv`) : 35 manquantes au global, **14 dans la fenêtre live** —
  le même lot de fiches joaillerie (sej et iv manquent ensemble sur ces 14).
- Joaillerie en fenêtre live : **13 fiches** (au-dessus du seuil de 10 fixé le
  20/08 — le chantier « trou du radar joaillerie » est satisfait pour l'instant
  ; ne pas ajouter de nouvelle fiche joaillerie tant que sej/iv des 13
  existantes ne sont pas complets).

## Publication

4 lots publiés au fil de l'eau, tous validés (`validate.py` : 0 bloqueur à
chaque fois) et poussés directement sur `main` (aucun repli sur branche
`claude/*` nécessaire). `healthcheck.sh` : http=200, date fraîche, 445/445
événements en ligne, cohérent.

## Analyse des visites

2 153 visiteurs aujourd'hui contre 1 987 hier (+8,4 %), cinquième jour de
hausse consécutif depuis le 21/08 (1 817 → 1 843 → 1 889 → 1 987 → 2 153) : une
progression régulière d'environ 5-8 % par jour, sans décrochage.

## Ce qui n'a pas pu être vérifié / reste ouvert

- **JustMe Porto Cervo** : signal préoccupant sur Xceed (aucun billet listé
  après le 24/08) — la date étendue à 07/09 est un buffer prudent, pas une
  confirmation ; à recontrôler en priorité demain.
- **Soirées Barrière Deauville** : aucune source officielle ne confirme
  l'existence même du programme sous ce nom — à requalifier ou retirer.
- **Été impérial Hôtel du Palais** : probable doublon avec « Été à l'Hôtel du
  Palais Biarritz » (même établissement, même saison) — à trancher (fusion ?).
- 44 fiches restent avec `iv.g`/`iv.w` en dérive « journal d'enquête »
  (≥1200 caractères) dans la fenêtre live — condensation à poursuivre.
- 14 fiches joaillerie en fenêtre live sans séjour ni invitation.
- L'artifact Claude de la doctrine (`89b85688-ff57-481d-82d7-f7792051b066`)
  reste introuvable (échec connu depuis le 21/08, consigné) — étape 10 non
  exécutée, sans conséquence pour le public (constanceparis7.com à jour).
- Branding « Été » toujours affiché (WARN non bloquant) — à proposer à
  Gérald/Constance pour le rafraîchissement « Automne ».

## Erreurs rencontrées

Aucune erreur d'outil. Deux corrections de fond apportées à la mémoire du site
(consignées dans `lessons.md` et `a-reverifier.md`) : une hypothèse non
vérifiée du 22/08 (Milan Ferragosto) et une convention de fiche permanente
(d2=2027-12-31) qui existait dans les données mais n'était écrite nulle part.
