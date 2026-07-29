# Compte rendu — passe du 29 juillet 2026 (cloud, radar-routine-claude)

## État général
- validate.py : OK — 0 blocker, 0 warning. 472 événements, 153 dans la fenêtre
  [aujourd'hui..+90j], traductions 472/472 (100%).
- perfcheck.py : OK — 0 régression (+0,01 Mo, +2 événements vs dernier point).
  Index allégé 0,43 Mo gzip, 12 langues différées servies par i18n-data/.
- KPI ACCÈS mondain (iv) : 192/352 (54%) — stable.
- Purge : 0 fiche à purger (aucun d2 < aujourd'hui−30j).
- Adresse publique https://constanceparis7.com : poussée sur main (commit 1b1d5f6f),
  eyebrow « 29 juillet 2026 ».

## Fait pendant la passe
1. **Backfill séjour (LOI DU SITE)** : 12 séjours composés pour des fiches de la
   fenêtre live sans `sej`, prestige d'abord — recherche web réelle, hôtels/tables/
   expériences vérifiés avec URL officielle :
   - Monaco (4) : les 2 concerts au Palais Princier (OPMC), clôture Laura Pausini
     et SOUL! du Monte-Carlo Summer Festival.
   - Ravello (5) : Götterdämmerung (Kent Nagano), Concerto all'alba, clôture Simon
     Rattle, Serate Jazz, Ditirambo Night (édition d'août).
   - Divers (3) : Soirée Blanche Four Seasons Megève, Hampton Classic Horse Show,
     Hublot Polo Gold Cup Gstaad.
   Compte des séjours : 112 → 126/472.
2. **2 nouvelles fiches nées complètes** (invitation + séjour + 12 langues dès la
   naissance, conformément à la LOI DU SITE) :
   - Dîner « Sous les Étoiles » — Villa Ephrussi de Rothschild (19 août 2026,
     Saint-Jean-Cap-Ferrat) : deux soirées uniques par an, dîner Robuchon Monaco
     dans les jardins du palais. Contact vérifié : accueil général 04 93 01 45 90
     (page officielle). Tarif non publié : indiqué comme tel, aucune invention.
   - Monte-Carlo Summer Festival — dîner-spectacle Lisa Stansfield (11 août 2026,
     Salle des Étoiles) : contacts SBM déjà vérifiés (mêmes canaux que SOUL!/Laura
     Pausini).
3. **Correction factuelle** : Festival de Ramatuelle — 42e édition → **41e édition**
   (vérifié festivalderamatuelle.com/ramatuelle-tourisme.com : le festival fêtait
   son 40e anniversaire en 2025). Correction répercutée dans `n` et dans les 12
   traductions (simple substitution numérique, pas de retraduction nécessaire).
4. **Vérification des 7 prochains jours** (recherche web) : Polo Parade
   Saint-Tropez, Jumping de Dinard, feu pyromélodique de Monaco et Délices Sonores
   confirmés tels quels. Festival de Ramatuelle : dates confirmées, édition
   corrigée (voir ci-dessus).
5. SEO : sitemap.xml lastmod=2026-07-29, ld+json enrichi (60 événements), 7320 URLs
   (gen_pages : 461 événements × 13 langues + hubs). 0 lien mort détecté (pages des
   2 nouvelles fiches + fiche renommée générées avant publication).
6. **Filet** : ajout de `.radar/tools/.lock` au `.gitignore` (fichier de verrou
   local, jamais destiné à être versionné — écarté d'un commit précédent).
   Rename de fiche : correction manuelle de `.last-names.json` pour refléter le
   renommage volontaire Ramatuelle (sinon `validate.py` bloque à tort en pensant
   à une perte de données — leçon consignée dans `lessons.md`).

## Événements des 48 h
- 29/07 (aujourd'hui) : Polo Parade sur le vieux port (Saint-Tropez) ; SOUL! An
  Exclusive Show, Salle des Étoiles (29-30/07 puis 3-9/08) ; Dîner « Sous les
  Étoiles » Villa Ephrussi (1ère des 2 soirées de l'année, ce soir).
- 30/07 : Jumping International de Dinard CSI 5*.
- 31/07 : Ravello Festival — Götterdämmerung (Kent Nagano).
- 1/08-12/08 : Festival de Ramatuelle, 41e édition.

## 3-5 nouveautés glamour
- Dîner « Sous les Étoiles » à la Villa Ephrussi de Rothschild — 19 août (nouvelle
  fiche, accès et séjour vérifiés).
- Lisa Stansfield en dîner-spectacle à la Salle des Étoiles, Monte-Carlo — 11 août
  (nouvelle fiche).
- Concerto all'alba du Ravello Festival — lever de soleil sur le Golfe de Salerne,
  5h15 sur le Belvédère de Villa Rufolo (séjour ajouté).
- Ditirambo Night au Caruso, A Belmond Hotel — dîner Ravello × Cilento, 26 août
  (séjour ajouté).
- Hublot Polo Gold Cup Gstaad, 44e édition — 20 août (séjour ajouté, GreenGo Club
  inclus).

## Visites (regard journaliste)
Le compteur public (GoatCounter) est resté illisible depuis cette session : la
politique d'egress réseau du conteneur cloud bloque l'accès direct à
goatcounter.com (même blocage que le 28/07 pour healthcheck). Aucun chiffre
inventé — le relevé du jour n'a pas pu être écrit dans `stats/visites.ndjson` ;
il sera rattrapé par le plancher GitHub Actions qui dispose du réseau. Rien à
commenter de neuf sur la fréquentation depuis cette session.

## Anomalies
1. **Réseau sortant bloqué depuis la session cloud** (confirmé, cf. leçon du
   28/07) : `relever_visites.py` → tunnel 403 ; `healthcheck.sh` → http=000000,
   alerte "site KO" générée. **Ce n'est PAS un site en panne** : c'est la sonde qui
   n'a pas de réseau depuis cette session. Aucun rollback déclenché (aurait été
   injustifié). Le vrai contrôle en ligne reste `.github/workflows/surveillance.yml`,
   qui dispose du réseau.
2. Aucune autre anomalie. Le repli sur branche `claude/*` n'a pas été nécessaire :
   le push sur `main` a été accepté directement.

## Auto-amélioration de la passe
- Correctif filet : `.radar/tools/.lock` ajouté au `.gitignore` (n'aurait jamais
  dû être un candidat au commit — fichier de concurrence purement local).
- Leçon consignée : un renommage volontaire de fiche (correction factuelle du nom)
  doit être répercuté manuellement dans `.last-names.json` pour ne pas déclencher
  un faux blocage « perte de données » dans `validate.py`.
