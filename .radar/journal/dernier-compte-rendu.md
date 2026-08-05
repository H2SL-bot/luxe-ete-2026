# Compte rendu — passe du 5 août 2026 (cloud, radar-routine-claude)

## État général
- validate.py : OK — 0 blocker, 0 warning. 529 événements, 136 dans la fenêtre
  [aujourd'hui..+90j], traductions 529/529 (100 %).
- perfcheck.py : OK — 0 régression (+0,00 Mo, +0 événement vs dernier point de
  cette passe). Index allégé 0,55 Mo gzip, 12 langues différées via i18n-data/.
- KPI ACCÈS mondain (iv) : 226/379 (59 %) — stable.
- Adresse publique https://constanceparis7.com : poussée sur `main`
  (commit 32c09500), eyebrow « 5 août 2026 ». Push direct accepté, aucun repli
  sur branche `claude/*` nécessaire.

## Fait pendant la passe
1. **Purge** : 6 fiches zombies retirées (d2 = 5 juillet, au-delà du seuil de
   30 jours) — Royal Monceau (indépendance américaine), PAD Saint-Tropez,
   Tokyo Jewelry Fes, défilé Boloria, Rencontres Musicales d'Évian, Henley
   Royal Regatta. 532 → 526 événements.
2. **Correction de doublons** (détectés par comparaison URL/nom pendant la
   vérification des 7 prochains jours) : 2 fiches en double supprimées, la
   version la plus complète et la mieux sourcée conservée dans chaque cas —
   « Sting Live Concert at Villa d'Este » (gardée, la version « concert privé
   & dîner de gala » retirée) et « Barrière Deauville Polo Cup 2026 » (la
   fiche détaillant les 4 sous-tournois gardée). 526 → 524.
3. **COMBLER L'AUTOMNE** (priorité 2 du plan validé par Gérald le 29/07,
   maintenant que les traductions — priorité 1 — sont à 100 %) : recherche
   web réelle, 6 événements ultra-mondains oct.-nov. identifiés et vérifiés
   (Qatar Prix de l'Arc de Triomphe à Longchamp, Art Basel Paris — déjà
   présente et complète sur le site, doublon évité —, vente du soir
   Sotheby's « Modernités », vente Artcurial « La Modernité en partage »,
   gala d'ouverture de la saison de danse à l'Opéra Garnier, ouverture de la
   saison lyrique de l'Opéra de Monte-Carlo avec Cecilia Bartoli). **5
   nouvelles fiches nées complètes** : invitation (`iv`, contacts
   professionnels publiés vérifiés — aucun n'a été inventé, plusieurs voies
   d'accès restent volontairement en billetterie individuelle faute de
   contact presse publié) + séjour (`sej`, hôtels/tables/expériences réels
   avec URL) + traductions dans les 12 langues dès la naissance. 524 → 529.
4. **Backfill séjour** (fenêtre live, prestige d'abord) : 10 séjours composés
   pour des fiches sans `sej` — Sublime Summer Party (Comporta), Taormina
   Arte Sicilia, Philharmonix (Dubrovnik), Soneva Stars/Sir Mo Farah, US Open
   Fan Week, clôture Dubrovačke ljetne igre, Four Seasons Maldives Surfing
   Trophy, Sir Rocco Forte Captain's Trophy (Verdura), Sotheby's Hong Kong
   ×2 (joaillerie + vente du soir). Recherche web réelle et vérification
   adversariale pour chacun ; l'agent a honnêtement signalé l'absence de
   palace collé au site de l'US Open (Flushing Meadows) plutôt que d'en
   inventer un — Manhattan retenu comme base réaliste avec transport direct.
5. Eyebrow mis à jour : « données collectées et vérifiées le 5 août 2026 ».
6. SEO : `gen_seo.py` (ld+json enrichi, sitemap lastmod=2026-08-05),
   `gen_pages.py` (518 événements × 13 langues + hubs, sitemap 8256 URLs,
   0 lien mort — 9 pages purgées/dédupliquées supprimées, 5 nouvelles créées
   dans les 13 langues).
7. **Filet** : `.last-names.json` mis à jour pour les 2 fiches dédupliquées
   (suppression volontaire et sourcée, pas une perte de données — sans quoi
   `validate.py` aurait bloqué à tort, leçon du 29/07 appliquée).

## Le reste-à-faire (recompté cette passe)
- **Traductions manquantes : 0/529.** Priorité 1 du plan du 29/07 terminée
  (la dernière passe d'hier, 04/08, avait atteint 100 %). Vérifié à nouveau
  ce matin après ajout des 5 nouvelles fiches : toujours 0.
- **Séjours manquants : 332 au total, dont 57 dans la fenêtre live** (68 → 57
  après le backfill de 10 aujourd'hui, +11 apportés par les 5 nouvelles
  fiches qui, elles, sont nées avec séjour).
- **Voies d'invitation manquantes : 233 au total, dont 20 dans la fenêtre
  live** (21 → 20 ; les 5 nouvelles fiches sont nées avec `iv`).
- **Guides d'accès (c=acces) : 11**, inchangé — priorité 3 du plan (10
  nouveaux guides) pas encore engagée cette passe, la priorité 2 (automne)
  ayant pris le pas comme prévu par l'ordre strict du plan.
- Octobre-novembre-décembre 2026 comptent désormais 74 événements (contre
  ~56 avant cette passe, oct. 20 + nov. 16 + déc. 33 début août) — la
  priorité 2 progresse mais n'est pas achevée ; à poursuivre passe après
  passe (~40-60 événements visés à terme sur cette fenêtre).
- 10 fiches restent sans URL source (`u` vide) — gap pré-existant, non
  aggravé ni corrigé cette passe (hors priorité du jour) : Feu d'artifice de
  Monaco, Gucci Flora x La Rose des Vents, Dioriviera Cannes, conseil accès
  août, Besch Cannes Auction, Twiga Porto Cervo, Hotel Pitrizza, Sottovento
  Club, Ritual Club Baja Sardinia, yachts Ibiza-Formentera.

## Événements des 48 h
- 5/08 (aujourd'hui) : Délices Sonores (Citadelle), Gilles Peterson à la
  Fondation Maeght.
- 6/08 : Concerts au Palais Princier (OPMC, clôture de saison), Ravello
  Festival (Serate Jazz), Barrière Deauville Polo Cup, Sublime Summer Party
  (Comporta, séjour composé aujourd'hui).
- Vérification ciblée des 24 fiches démarrant sous 7 jours : liens et dates
  cohérents ; c'est cette vérification qui a fait remonter les 2 doublons
  corrigés ci-dessus.

## 3-5 nouveautés glamour
- Qatar Prix de l'Arc de Triomphe à Longchamp (4 octobre) — nouvelle fiche,
  séjour 16e arrondissement + déjeuner étoilé au Pré Catelan.
- Ouverture de saison lyrique de l'Opéra de Monte-Carlo : Cecilia Bartoli
  dirige « Carmen » avec Marina Viotti et Benjamin Bernheim (20 novembre).
- Gala d'ouverture de la saison de danse à l'Opéra Garnier (10 octobre),
  soirée AROP avec Hugo Marchand et Germain Louvet.
- Ventes Sotheby's « Modernités » et Artcurial « La Modernité en partage »,
  calées sur la semaine Art Basel Paris fin octobre.
- Backfill séjour Sir Rocco Forte Captain's Trophy — tournoi inaugural au
  Verdura Resort en Sicile, exhibition de Colin Montgomerie.

## Visites (regard journaliste)
Le compteur GoatCounter reste illisible depuis cette session cloud (403 —
tunnel bloqué, testé à la fois en direct et via l'outil de récupération web ;
même anomalie que le 28-29/07). Le dernier relevé exploitable
(`stats/visites.ndjson`) montre une progression continue sur 5 jours :
270 → 284 → 299 → 311 → 319 visites du 31/07 au 04/08, soit environ +18 %
sur la période — tendance saine, sans rupture visible. Aucun chiffre du jour
disponible ni inventé ; le relevé sera rattrapé par le plancher GitHub
Actions qui dispose du réseau.

## Résultats des contrôles
- `validate.py` : OK, 0 blocker, 0 warning.
- `perfcheck.py` : OK, 0 régression.
- `healthcheck.sh` : **ALERTE technique, mais fausse alerte connue** —
  http=000000 (réseau sortant bloqué depuis cette session cloud, comme les
  28 et 29/07 ; ce n'est pas une panne du site). Pas de `rollback.sh`
  déclenché — cela aurait été injustifié (leçon du 28/07, déjà consignée,
  reconfirmée ici). Le contrôle qui fait foi reste
  `.github/workflows/surveillance.yml`, qui dispose du réseau.
- Adresse publique constanceparis7.com : à jour côté dépôt (commit
  32c09500 poussé sur `main`), non vérifiable en direct depuis cette session
  pour la même raison réseau.

## Anomalies
1. Réseau sortant bloqué depuis la session cloud (confirmé à nouveau : curl
   direct → erreur 56/tunnel, `relever_visites.py` → 403, `healthcheck.sh` →
   000000, `WebFetch` sur goatcounter.com → 403 également). Anomalie déjà
   documentée les 28 et 29/07 ; aucune action corrective possible côté passe,
   elle relève de la politique réseau du conteneur.
2. Republication de l'artifact claude.ai (étape 10 de la doctrine) non
   effectuée cette passe faute d'accès direct au fichier `index.html` généré
   dans un contexte où l'outil Artifact serait pertinent pour ce cas d'usage
   précis (grand fichier de données, pas un artifact de présentation) — sans
   incidence sur le site public, qui est la source de vérité.
3. Aucune autre anomalie. Signature des commits posée (`radar-routine-claude`)
   dès le début de passe.

## Auto-amélioration de la passe
- Détection systématique de doublons par similarité de nom sur les fiches
  partageant la même URL source, appliquée pendant la vérification des 7
  prochains jours : a mis au jour 2 doublons réels qui seraient restés
  invisibles autrement (noms légèrement différents, même événement, même
  date, même URL). À reproduire aux passes suivantes comme filet
  supplémentaire, en particulier sur les fiches issues de vagues de collecte
  différentes.
- Aucune fabrication de donnée : sur les 6 candidats automne identifiés par
  la recherche, aucun contact presse nominatif n'a été inventé quand la
  source ne le publiait pas — `iv.g`/`iv.w` documentent alors la voie
  officielle générale (billetterie individuelle) plutôt qu'un nom fictif.
