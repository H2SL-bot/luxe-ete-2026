# Compte rendu — passe du 20 août 2026 (cloud, radar-routine-claude)

## Cadence
Passe normale (dernière passe complète tracée : 19/08, ~24 h d'écart, sous le seuil de
30 h). `precheck.sh` n'a signalé aucune anomalie de démarrage.

## Réseau : WebFetch et curl toujours bloqués, WebSearch non sollicité
Testé en tout début de passe sur wikipedia.org et google.com : `curl -sL` → `000`
(timeout de la passerelle), `WebFetch` → `EGRESS_BLOCKED`. Même schéma que les 11-13/08
et le 19/08. Aucune recherche web n'a été nécessaire cette passe (priorité condensation,
voir plus bas), donc aucun impact réel — mais cela a aussi empêché le relevé quotidien
GoatCounter (`relever_visites.py` : « compteur illisible aujourd'hui », aucune ligne
écrite pour le 20/08 dans `stats/visites.ndjson`).

## PRIORITÉ DU JOUR — condensation des voies d'invitation (`iv.o`/`iv.g`/`iv.w`)
Conformément à la consigne prioritaire : la dérive « journal d'enquête » touchait 255
fiches au 19/08 (159 dans la fenêtre live). Deux vagues de 20 fiches condensées et
publiées aujourd'hui, en commençant par les plus imminentes de la fenêtre live :

- **Vague 1** (critère de sélection : un champ ≥ 400 car., cible de rédaction) : 20
  fiches, dont White Party Casino Barrière, Dîner Ayla Privé, Meeting hippodrome de la
  Canche (Le Touquet), Prix Morny, Clair-obscur (Bourse de Commerce), Les Nocturnes de
  la Villa Ephrussi, Calvin Harris (Ushuaia Ibiza)…
- **Vague 2** (critère de sélection corrigé : un champ ≥ 1200 car., seuil WARN réel de
  `validate.py` — voir leçon ci-dessous) : 20 fiches supplémentaires, dont Les Caves du
  Roy, Twiga Porto Cervo, Torneo de Polo de Sotogrande, Meeting de Deauville Barrière
  (fiche + billetterie), Nikki Beach Saint-Tropez, Hôtel du Cap-Eden-Roc, Grand Hôtel de
  Cala Rossa, et les deux fiches DG Resort/Casa Amor (doublon connu, voir plus bas).

**40 fiches condensées au total** (double de la cible quotidienne de 15-20, budget de
session le permettait). Méthode : chaque champ relu et réécrit par un agent dédié,
tout fait vérifié conservé intégralement (noms, fonctions, e-mails, téléphones,
adresses, URLs, tarifs, horaires, dates limites), seules les tournures d'enquêteur et
les redites entre champs supprimées. Aucun fait n'a été inventé ni retiré. Chaque lot
réinjecté avec vérification du NOM (pas seulement de l'indice) avant écriture, puis
`split_i18n.py --apply` → `gen_seo.py` → `gen_pages.py` → `validate.py` → publication.

**Résultat mesuré** (`validate.py`, seuil WARN 1200 car.) : `iv.g` 120 → 98 fiches en
excédent (excédent total 89 585 → 71 057 car.), `iv.w` 137 → 118 fiches (134 565 →
114 170 car.). `iv.o` reste propre (0 WARN).

**Reliquat** : 254 fiches ont encore un champ ≥ 400 car. (179 dans la fenêtre live) ;
129 fiches ont encore un champ ≥ 1200 car., le signal fiable de dérive réelle (101 dans
la fenêtre live). À poursuivre par lots de 15-20 aux prochaines passes.

## Leçon ajoutée au filet
Le critère de sélection ≥ 400 caractères (qui est la CIBLE de rédaction, pas un seuil de
dérive) a fait resélectionner en vague 2 presque les mêmes fiches que la vague 1 : une
fiche condensée qui garde plusieurs contacts nominatifs distincts reste légitimement
au-dessus de 400 caractères. Corrigé en cours de passe : sélection par le seuil WARN de
`validate.py` (≥ 1200 car.), qui identifie la vraie dérive « journal d'enquête » sans
resélectionner du travail déjà fait. Détail dans `.radar/tools/lessons.md` (20/08/2026).

## Purge
1 zombie purgé : « Exposition Pomellato 'Le Joaillier révolutionnaire' au Palais de
Tokyo » (d2 = 2026-07-20, > 30 j). 434 → 433 fiches.

## État de la LOI DU SITE (traductions / séjours / invitations)
`reste.py` : traductions 433/433 (100 %) ; séjours 368/433 (65 manquants) ; invitations
415/433 (18 manquants). Vérification par script (croisement `d2 ≥ aujourd'hui`) : **les
65 séjours et les 18 invitations manquants sont tous des fiches déjà passées** (gardées
30 jours avant purge, hors fenêtre visible par le voile d'affichage). **La fenêtre live
(94 événements) reste à 100 % séjours et 100 % invitations.** Aucun backfill lancé — la
priorité du jour (condensation) restait la bonne cible, conformément à la consigne.

## Doublon connu, non traité cette passe
`.radar/a-reverifier.md` signale toujours le doublon « DG Resort 2026 à Saint-Tropez —
Casa Amor » (idx 74) / « Dolce & Gabbana x Casa Amor — takeover 'DG Resort' » (idx 75) :
même opération, mêmes dates (01/07-30/08), même lieu. Les deux ont été condensées
aujourd'hui (elles avaient chacune une dérive), mais la fusion elle-même n'a pas été
faite par prudence budgétaire — un merge de fiche à 12 langues demande une relecture
complète des deux jeux de traductions pour ne perdre aucun fait. À faire à une passe
dédiée : garder la fiche la plus complète (idx 75, qui a déjà l'adresse corrigée
« chemin de la Matarane » et un numéro de téléphone que idx 74 n'a pas), reprendre tout
fait exclusif de l'autre, supprimer le doublon, mettre à jour `.last-names.json`.

## Recherche de nouveaux événements
Aucune cette passe, conformément à la priorité explicite du jour (condensation avant
recherche de neuf).

## Analyse des visites
Le relevé du jour n'a pas pu être fait (réseau bloqué). Sur les 5 derniers jours
disponibles (14→19/08) : 426 → 458 → 478 → 631 → 1 046 → 1 711 visites/jour — une
progression continue qui a plus que quadruplé en cinq jours. Aucun détail par page ou
par pays disponible aujourd'hui (tableau GoatCounter injoignable) ; à recroiser à la
prochaine passe avec réseau disponible.

## Contrôles
`validate.py` : OK — 0 blocker(s), 2 warning(s) (iv.g/iv.w, en baisse, voir plus haut).
`perfcheck.py` : OK — 0 régression (poids page 1,08 Mo gzip, en légère baisse grâce à la
condensation malgré 40 fiches retouchées).
Publication : 5 commits poussés directement sur `main` (démarrage, purge zombie, journal
perfcheck, condensation vague 1, condensation vague 2) — aucun repli sur branche
`claude/*` nécessaire aujourd'hui, le push direct sur `main` a fonctionné à chaque fois.
Adresse publique : https://constanceparis7.com — inchangée.

## Anomalies
- Réseau : `curl`/`WebFetch` bloqués toute la passe (voir plus haut) — sans impact sur
  le travail du jour, mais empêche tout test de lien direct et le relevé de visites.
- Rien d'autre à signaler.
