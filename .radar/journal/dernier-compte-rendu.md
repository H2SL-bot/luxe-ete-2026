# Compte rendu — passe du 19 août 2026 (cloud, radar-routine-claude)

## Rattrapage de cadence
`precheck.sh` a signalé une CADENCE ROMPUE : dernier run journalisé il y a 161 h
(> 30 h). Aucune passe complète tracée entre le 13/08 et le 18/08 (le 18/08 a
vu la passation Gérald → Constance et un travail d'outillage, pas une passe
quotidienne au sens de la doctrine — pas de ligne FIN dans `passages.log`, pas
de compte rendu). Cette passe du 19/08 est donc une passe de RATTRAPAGE
complète, exécutée selon la procédure de `DOCTRINE.md`.

## Réseau : WebFetch et curl bloqués en bloc, WebSearch opérationnel
Testé en tout début de passe sur des domaines témoins neutres (wikipedia.org,
google.com, le compteur GoatCounter) : `curl` direct → `000` (passerelle),
`WebFetch` → `EGRESS_BLOCKED` sur tous les domaines, confirmé par
`$HTTPS_PROXY/__agentproxy/status` (403 de politique). `WebSearch`, lui, a
fonctionné normalement toute la passe et a permis tout le travail ci-dessous.
Conséquence assumée : aucun test de lien par requête directe (retest hebdo du
lundi non applicable aujourd'hui — mercredi), aucune lecture de page brute ;
tout s'est appuyé sur `WebSearch` avec recoupement de sources.

## État de la LOI DU SITE : bonne nouvelle chiffrée
`reste.py` affiche encore 66 séjours et 18 invitations manquants sur 434
fiches. Vérification par script (croisement avec `d2 >= aujourd'hui`) : les
66 et les 18 sont **tous des événements déjà passés** (gardés 30 jours avant
purge, hors fenêtre visible par le voile d'affichage). **La fenêtre live
(aujourd'hui → +90 jours, 96 événements) est à 100 % séjours et 100 %
invitations** — la LOI DU SITE est honorée sur tout ce qu'un visiteur voit
réellement. Aucun backfill n'a donc été lancé sur des fiches déjà passées :
ça n'aurait servi personne. Zéro zombie à purger (`d2 < aujourd'hui-30j`).

## Nouvelle destination : Melbourne (carte des destinations à conquérir)
Composé, vérifié par un agent adverse dédié, puis traduit en 12 langues :
**« Lexus Melbourne Cup Day 2026 — le Birdcage, Flemington »** (mardi 3
novembre 2026, Flemington Racecourse). Née COMPLÈTE dès la publication :
- **Invitation (`iv`)** : voie gratuite réelle mais restrictive (accréditation
  presse nominative, Media Accreditation Unit du Victoria Racing Club,
  candidatures ouvertes début septembre) honnêtement qualifiée comme telle ;
  voie payante (Birdcage Reserved, tables, marquees de sponsors dès 1895 AUD/
  pers., seul tarif confirmé par recoupement — les deux autres montants trouvés
  en première recherche n'ont pas pu être corroborés indépendamment, donc
  retirés du texte final plutôt que publiés sur une seule source) ; contacts
  strictement génériques (ligne VRC, boîte presse), aucun nom de personne
  fabriqué, conformément au garde-fou absolu.
- **Séjour (`sej`)** : Crown Towers Melbourne et Park Hyatt Melbourne
  (palaces réels), Vue de Monde et Attica (trois toques Good Food Guide —
  le texte précise explicitement que le Michelin ne note pas l'Australie,
  pour ne jamais laisser croire à une étoile inventée), Fashions on the
  Field comme expérience.
- Vérification adverse dédiée (agent séparé, mandat de réfutation) : verdict
  FIABLE, une réserve mineure (deux tarifs non confirmables) traitée par
  retrait du texte plutôt que par maintien d'un doute.
- Ville « Melbourne » ajoutée au registre `villes-i18n.json` (12 langues).
- 434 fiches désormais (433 → 434).

## Filet — amélioration trouvée et corrigée
Contrôle manuel du 12/08 (`iv.o` > 1200 car. = journal d'enquête) : re-testé
sur la nouvelle fiche, `iv.o` était propre (1003 car.) mais `iv.g` faisait
2521 car. et `iv.w` 3292 — la même dérive avait migré vers des champs non
surveillés. Chiffrage global : **121 fiches avec `iv.g` > 1200 car.**
(excédent 89 585 car., jusqu'à 3 924 sur une seule fiche) et **137 fiches
avec `iv.w` > 1200 car.** (excédent 134 565 car., jusqu'à 6 001 sur une
fiche) — invisibles du filet depuis le 12/08. `validate.py` étend désormais
le même contrôle WARN (non bloquant) aux trois champs `o`/`g`/`w`. Condensation
reportée par lots aux prochaines passes (comme pour `iv.o` avant elle) : un
traitement de masse à la main risquerait une erreur de contact.

## Registre de ré-audit nettoyé
`.radar/a-reverifier.md` portait 176 cases à cocher, dont 4 concernaient des
fiches déjà tranchées ailleurs (Via Notte et Alemagou retirés le 11-12/08,
Ginza Le Studio retiré le 18/08, une exposition Chanel 19M sortie de la
fenêtre par purge normale) — supprimées comme doublons résolus. **172
cases restent ouvertes**, dont 116 concernent des événements encore dans la
fenêtre live : c'est le plus gros chantier en attente du site. Spot-check de
4 fiches parmi les plus imminentes (Jesus Christ Superstar Singapour,
Laurent Wolf/Deauville, Singapore Night Festival, dîner Ayla Privé Bodrum) :
les 4 confirmées exactes par recherche indépendante, aucune erreur trouvée —
signal positif sur la qualité globale, mais un ré-audit complet des 116
fiches n'a pas pu être fait cette passe (à poursuivre par lots de 8-10).

## Contrôles
- `validate.py` : **OK — 0 blocker, 2 warnings** (iv.g/iv.w, voir ci-dessus).
- `coherence_i18n.py` : OK, 0 divergence sur 434 fiches.
- `gen_seo.py` + `gen_pages.py` régénérés, eyebrow déjà à jour (19 août 2026).
- Traductions manquantes : **0/434** (100 %).
- Séjours manquants (fenêtre live) : **0/96**. Invitations manquantes
  (fenêtre live) : **0/96**.
- KPI ACCÈS mondain (`iv`) : 294/299 (98 %).
- Fiches sans lien officiel `u` (fenêtre live) : 6 — toutes des fiches
  saisonnières/conseil à sources multiples (`so`), pas d'URL canonique
  unique par nature ; non anormal.
- `healthcheck.sh` : lancé, mais le blocage réseau documenté depuis le 11/08
  (curl direct → 000) rend la sonde aveugle depuis une session cloud — pas de
  rollback déclenché sur cette base, conformément à la leçon du 28/07.
- Publication : `bash .radar/session/publier.sh` → **POUSSÉ** directement sur
  `main` (commit `446ae13`), aucun repli sur branche `claude/*` nécessaire.

## Analyse des visites
GoatCounter (compteur JSON, tableau complet) inaccessible ce jour — même
blocage réseau que le reste de la session (`EGRESS_BLOCKED`). Aucun chiffre
inventé ; relevé du jour non écrit dans `stats/visites.ndjson`. D'après le
dernier repère connu (7→13 août : 341 → 401 visites/jour, ~+3 %/jour), rien
ne permet de dire si la tendance s'est maintenue pendant l'absence de passes
(14-18 août).

## Point d'attention pour Constance (pas d'action requise)
La ligne d'édition affiche toujours « Juillet et août 2026 ». La doctrine
prévoit de proposer un rafraîchissement « Automne 2026 » vers le 25 août,
sans renommer seul : à remettre à l'ordre du jour dans quelques jours.

## Ce qui reste pour la prochaine passe
- Poursuivre le ré-audit des 116 fiches live de `a-reverifier.md` (lots de
  8-10, via WebSearch tant que WebFetch reste bloqué).
- Condenser les fiches `iv.g`/`iv.w` les plus longues (121 + 137 fiches).
- Poursuivre l'ajout de destinations de la carte encore absentes (Lac de
  Côme, Comporta/Melides, Riviera d'Athènes/Spetses, Dubrovnik, Mustique,
  Harbour Island, Casa de Campo, Riyad/AlUla).
- Retester les liens (prochain lundi, si le réseau répond) et réessayer
  GoatCounter.
