# Compte rendu — passe du 13 août 2026 (cloud, radar-routine-claude)

## Anomalie n°1 — réseau sortant totalement bloqué (confirmé, pas un incident de site)
Dès le premier test (domaine témoin sans rapport, `wikipedia.org`), la sortie
réseau a répondu `EGRESS_BLOCKED` — un refus explicite de la politique de
cette session, pas un timeout ambigu. Conséquence directe et assumée : **aucune
recherche web, aucune vérification de lien, aucun nouvel événement, aucun
backfill séjour/invitation n'a pu être fait cette passe** — la règle absolue
du site (jamais de donnée non vérifiée) l'interdit sans accès aux sources.
Même diagnostic pour `stats/visites.ndjson` (compteur GoatCounter illisible,
`403`, rien écrit) et pour `healthcheck.sh` en fin de passe (`http=000000`) :
signature déjà rencontrée les 11 et 12/08, reconnue comme faux-négatif réseau
et non comme échec de publication — **`rollback.sh` non lancé, à raison**.

## Travail effectué malgré le réseau bloqué (mécanique + rédactionnel, sans web)
- **Purge de 4 zombies** (d2=2026-07-13, événements ponctuels du 13 juillet
  largement dépassés) : dîner feu d'artifice Shangri-La, soirée Langosteria
  au Cheval Blanc, croisières de gala sur la Seine, dîner en Blanc du
  Centenaire — Hôtel Barrière. 463 → **459 fiches**.
- Date de l'eyebrow mise à jour (13 août 2026).
- `python3 tools/gen_seo.py` + `tools/gen_pages.py` régénérés (sitemap 7307
  URLs, 0 lien mort attendu), `coherence_i18n.py` : OK, 0 divergence.
- **Amélioration du filet — bug de cadence corrigé.** `precheck.sh` comparait
  l'écart depuis le dernier run à un seuil de 14 h, hérité de l'époque
  « 2 passes/jour ». Depuis la suppression de la passe du soir (22/07), la
  cadence nominale est 1 passe/jour (~24 h d'écart normal) : ce seuil
  déclenchait donc une fausse alerte « CADENCE ROMPUE » à CHAQUE passe,
  y compris ce matin (23 h d'écart, aucune passe manquée). Seuil relevé à
  30 h. Leçon consignée dans `lessons.md`.
- **Auto-amélioration perf — condensation de 6 fiches `iv.o`/`iv.g`.** Le
  problème signalé les 11 et 12/08 (le champ visiteur `iv.o` avait dérivé en
  journal d'enquête complet du contrôleur sur des fiches récemment
  contrôlées) avait EMPIRÉ entre les deux dernières passes (115→138 fiches en
  excès, +38 % de poids). Condensé à la conclusion + contacts vérifiés (noms,
  fonctions, emails, téléphones professionnels publiés — en excluant
  explicitement tout numéro que la source elle-même marquait « à ne jamais
  republier ») pour 6 fiches parmi les plus lourdes : Capri (Anema e Core),
  Dior Spa Cheval Blanc, Villa Louis Vuitton, POINT D'ENTRÉE lieux-scènes,
  POINT D'ENTRÉE ventes aux enchères, Scene yacht Ibiza-Formentera.
  Résultat : 138 → **132 fiches** encore en excès, excédent cumulé
  210 630 → **189 939** caractères, poids gzip 1,11 → **1,09 Mo**. Travail
  volontairement limité à ce lot pour vérifier chaque contact à la main sans
  erreur (risque réel : republier par erreur un numéro personnel non
  autorisé) — le reste (126 fiches) est reporté aux prochaines passes.

## État général et contrôles
- `validate.py` : **OK — 0 blocker, 1 warning** (132 fiches `iv.o` encore
  > 1200 caractères, en baisse — voir ci-dessus).
- `perfcheck.py` : **régression toujours signalée** — poids gzip 1,09 Mo
  contre seuil 0,83 Mo (base 0,69 Mo). Cause identifiée et pas aggravée par
  cette passe (voir ci-dessus) ; en résorption progressive, pas résolue en
  une passe vu le volume (126 fiches restantes) et le besoin de vérifier
  chaque contact à la main.
- Traductions manquantes : **0 / 459** (100 % traduit).
- Séjours manquants (hors fiches-conseil) : **124** (contre 188 le 12/08).
- Invitations manquantes (`iv` vide) : **63** (contre 92 le 12/08).
- Fenêtre automne (fiches débutant oct./nov./déc.) : **73** — le trou
  d'automne signalé fin juillet est désormais comblé par les passes
  précédentes.
- KPI ACCÈS mondain (`iv`) : **283/319 (88 %)**.
- Fiches sans lien officiel `u` : **10** — non retestées ce jour (réseau).
- Adresse publique https://constanceparis7.com : commit poussé directement
  sur `main` (`be5bbf2b`), pas de repli sur branche `claude/*` nécessaire.
  Propagation CDN non vérifiable ce jour (réseau bloqué côté sonde).

## Analyse des visites
Compteur GoatCounter illisible aujourd'hui (réseau bloqué) — aucun chiffre
inventé, relevé du jour non écrit. D'après les 6 derniers jours déjà
enregistrés (7→12 août) : progression continue et régulière, 341 → 353 → 365
→ 380 → 390 → 401 visites/jour (~+3 %/jour). Rien ne permet de dire si la
tendance s'est poursuivie le 13.

## Ce qui n'a PAS été fait cette passe (report)
Recherche de nouveaux événements, vérification des liens (dont les 10 fiches
sans lien `u`), backfill des 124 séjours et 63 voies d'invitation restants,
traductions par lot, condensation des 126 fiches `iv.o` restantes : rien de
tout cela n'a été possible faute d'accès réseau. Priorité inchangée pour la
prochaine passe si le réseau répond : séjours et invitations manquants
(124 / 63), poursuite de la condensation `iv.o`/`iv.g` (perfcheck reste en
régression tant que le poids n'est pas repassé sous ~0,83 Mo).

## Traces
`git push` direct sur `main` accepté aux deux étapes (démarrage + publication
finale) — aucune session concurrente détectée, aucun repli sur branche
`claude/*` nécessaire.
