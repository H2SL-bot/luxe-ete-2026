# Compte rendu — passe du 06/09/2026

## Priorité du moment : condensation des voies d'invitation — chantier vérifié quasi soldé

Contrôle exhaustif fait ce jour : seules **10 fiches** dépassent encore le seuil WARN de
1200 caractères sur `iv.o`/`iv.g`/`iv.w` (1 champ `iv.g` + 10 champs `iv.w`, avec
recoupement). J'ai **relu intégralement le texte des 10** (POINT D'ENTRÉE ventes aux
enchères, Formula 1 Abu Dhabi GP, Yves Saint Laurent and Photography/ICP, Gstaad New
Year Music Festival, Grand Hôtel de Cala Rossa, Villa Carmignac, Biennale Arte 2026,
Saint-Barth Cata Cup, Dubai Racing Carnival, Scene yacht Ibiza-Formentera) pour trancher
dérive réelle vs contenu légitimement dense (méthode des leçons du 20-21/08).

**Verdict : aucune dérive « journal d'enquête ».** Les dix textes s'adressent au
visiteur, sans tournure d'enquêteur, sans titre de section numéroté, sans commentaire de
méthode, sans redite entre `o`/`g`/`w`. Ils restent au-dessus de 1200 caractères parce
qu'ils portent légitimement de nombreux faits distincts et vérifiés (jusqu'à une dizaine
de contacts, tarifs ou horaires par fiche — ex. la grille tarifaire complète de l'ICP
avec 8 paliers d'adhésion, ou les 13 ventes du calendrier Christie's Paris). J'ai aussi
recherché systématiquement les marqueurs de dérive doctrinaux (« OUI, une voie existe,
mais… », « CE QUE LA MAISON MET RÉELLEMENT… », titres numérotés, jargon de vérification)
sur l'ensemble des 392 fiches : aucune occurrence restante. **Le défaut signalé le
12-19/08 (255 fiches touchées) est donc traité à zéro dérive résiduelle** — ce que
confirme la trajectoire des passes précédentes (255 → 121/137 → ... → 11 → 10
aujourd'hui, chaque lot condensé restant légitimement dense ensuite).
Aucune fiche condensée aujourd'hui : il n'y avait rien à condenser sans perdre un fait,
ce qui serait contraire à la règle « on ne supprime aucun fait ».

## Plancher du jour (purge, liens, date)

`passe_automatique.py --apply` : purge de **3 zombies** (d2=06/08/2026, franchi le seuil
des 30 jours aujourd'hui même — Gilles Peterson/Impressions, Concerts au Palais
Princier/Kazuki Yamada, Sublime Summer Party), **119 liens testés** sur les plus
imminents (0 mort), eyebrow mis à jour au 6 septembre 2026. Publié en premier via
`publier.sh` (0 blocker), avant tout le reste — c'est le socle qui débloquait `validate.py`
(3 zombies bloquaient la publication en tout début de passe).

## LOI DU SITE — recomptée sur la fenêtre live (aujourd'hui → +90j)

| | fenêtre live |
|---|---|
| Traductions manquantes (13 langues) | 0 |
| Séjours manquants | **0** |
| Invitations manquantes | **0** |

100 % honoré sur ce qui est réellement montré aux visiteurs (392 fiches au total, dont
97 dans la fenêtre live ; les 19 séjours et 4 invitations manquants au global sont tous
hors fenêtre — événements déjà passés conservés 30 jours, ou au-delà de +90 jours).
Joaillerie : **15 fiches en fenêtre live** (seuil de vigilance de la doctrine : 10) — le
trou signalé le 20/08 reste comblé.

## Recherche de nouveauté : Bal de la Rose de Monte-Carlo — non publiable, honnêtement

Recherche complète (organisateur, contact de réservation, tarif indicatif, séjour
palace/table/expérience, code vestimentaire) sur le Bal de la Rose du Sporting
Monte-Carlo, absent du site et identifié dans `CHANTIERS.md` comme cible d'élargissement
printemps 2027. **Aucune date 2027 n'est encore annoncée** (vérifié directement sur
montecarlosbm.com : la 70e édition, seule confirmée, s'est tenue le 21/03/2026).
Conformément au garde-fou anti-fabrication, je n'ai pas deviné de date ni créé de fiche.
Tous les autres faits (organisateur SBM/Fondation Princesse Grace, contact réservation,
tarif indicatif ~1800 €/pers. — presse, non officiel —, séjour Hôtel de
Paris/Hermitage/Monte-Carlo Bay + Louis XV/Blue Bay + Casino/Thermes Marins, tenue black
tie) sont consignés dans `.radar/CHANTIERS.md` (chantier 08) pour une naissance complète
dès l'annonce officielle de la date, probablement en fin d'année 2026.

## Autres vérifications faites ce jour

- **Grand Prix de Monaco 2027** : statut « sous réserve d'approbation FIA » reconfirmé
  par recherche web (annonce du calendrier 2027 attendue à l'automne 2026) — aucun
  changement à la fiche.
- **JustMe Porto Cervo** (doute ouvert le 20/08, d2=07/09 demain, nom inquiétant « Mamacita
  Closing Party ») : tentative de revérification via WebFetch — page rendue côté client,
  aucune date d'événement lisible par cette méthode. Doute non tranché, laissé ouvert
  dans `a-reverifier.md` ; sans conséquence pratique immédiate (la fiche sort de la
  fenêtre live dès demain de toute façon).
- `.radar/a-reverifier.md` (20 doutes ouverts, dont plusieurs avec des `d2` déjà dépassés
  ou très proches) : pas repris intégralement aujourd'hui, faute de temps — signalé pour
  une prochaine passe, le fichier commence à redevenir volumineux (428 lignes).

## Mémoire et visites

- `memoire.py changements` : 0 changement de date consigné sur 7 jours.
- Visites : **2529** aujourd'hui contre 2519 hier (+0,4 %), progression continue et
  régulière depuis 8 jours (2388 → 2529, soit +5,9 %). Pas de rupture ni de pic. Pas de
  recoupement pays/source fait aujourd'hui (aucun outil de répartition public disponible
  au-delà du compteur total GoatCounter).

## Ce qui n'a pas pu être vérifié / reste en suspens

- Le rafraîchissement de saison « Été » → « Automne » reste en attente depuis fin août :
  décision qui appartient à Constance (branding jamais touché seul).
- `a-reverifier.md` : reprise complète différée, fichier à re-consolider bientôt (lesson
  du 20/08 : un registre qui s'allonge sans dédoublonnage devient illisible).
- Bal de la Rose 2027 : à reprendre dès l'annonce officielle de la date (voir ci-dessus).

## Contrôles finaux

`validate.py` : 0 blocage, 3 avertissements (les 10 fiches `iv` légitimement denses +
1 rappel de saison). `healthcheck.sh` : OK (http=200, compte live=392=attendu, date
fraîche). Publication faite en 2 commits sur `main` (plancher, relevé de visites), aucun
repli de branche nécessaire aujourd'hui.
