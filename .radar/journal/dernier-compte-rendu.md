# Compte rendu — passe du 11 août 2026 (cloud, radar-routine-claude)

## Anomalie de déclenchement — À SIGNALER EN PREMIER
`precheck.sh` a détecté une **cadence rompue : 152 h depuis le dernier
« DEMARRAGE » journalisé** (dernier passage complet le 5 août à 03:56 UTC,
celui-ci le 11 août à 12:29 UTC — 6 jours d'écart au lieu d'un par jour).
Cette passe est donc une **passe de RATTRAPAGE**. Rassurant : le site n'a PAS
été laissé à l'abandon pendant ces 6 jours — la « passe quotidienne
automatique » (plancher, signature `radar-passe-quotidienne`) a tourné tous
les jours (5, 6, 7, 8, 9, 10, 11 août), a tenu l'eyebrow à jour et a fait de
l'entretien/vérification de liens. Ce qui n'a PAS eu lieu pendant ces 6 jours,
faute du passage de cette routine complète : recherche de nouveaux événements,
backfill séjour/invitation, dédup, traduction. Origine du décrochage non
identifiable depuis cette session (pas d'accès aux réglages de déclenchement) —
signal à vérifier côté ordonnanceur si l'écart se reproduit.

## État général
- `validate.py` : **OK — 0 blocker, 0 warning.** 482 événements, 120 dans la
  fenêtre [aujourd'hui..+90j], traductions 482/482 (100 %).
- `perfcheck.py` : **OK — 0 régression** (poids inchangé, -47 événements par
  rapport au dernier point enregistré — purges normales du plancher pendant
  l'absence, pas une perte de données : `validate.py` ne bloque que sur une
  fiche non périmée qui disparaîtrait, ce qui n'est pas le cas ici).
- KPI ACCÈS mondain (`iv`) : 224/336 (66 %) — stable ; les voies d'invitation
  ajoutées cette passe (US Open, Polo Gassin, Le Marois, Touquet) ne comptent
  pas dans cet indicateur car leurs catégories ne sont pas classées « mondain »
  par `validate.py` — utile quand même pour la promesse d'accès du site.
- Adresse publique https://constanceparis7.com : poussée sur `main` (commit
  `80cd6d3`), push direct accepté, aucun repli sur branche `claude/*`
  nécessaire.

## Fait pendant la passe
1. **Dédup de 2 doublons réels**, détectés par comparaison URL+dates lors de
   l'audit de la fenêtre live : « Arqana - La Vente d'Août » (deux fiches
   identiques pour la même vente de yearlings 15-17 août, gardé la version
   avec le contact presse le plus complet) et « Palermo-Montecarlo 2026 »
   (deux fiches pour la même régate 18-23 août, gardé la version avec `iv`
   déjà renseigné et le mieux sourcée). 484 → 482. `.last-names.json` mis à
   jour en conséquence pour ne pas déclencher de faux blocage.
2. **7 guides d'accès intemporels sauvés d'une purge involontaire** : les
   fiches « POINT D'ENTRÉE — … » (c=acces) avaient un `d2` daté de juillet
   2026 alors que la doctrine les veut intemporelles ; elles auraient disparu
   du site fin août au prochain seuil de purge à 30 jours. `d2` repoussé à
   fin 2027. Aucun contenu modifié, seulement la date d'expiration technique.
3. **4 séjours composés** (recherche web réelle, calibre jet-set, aucune
   fabrication) : Regata Palermo-Montecarlo (côté Monte-Carlo, Hermitage/Hôtel
   de Paris, Le Louis XV, Yacht Club de Monaco), Dîner de Ferragosto au
   Quisisana (sur place à Capri, Da Paolino, La Fontelina, Villa San Michele),
   Chantilly Arts & Élégance (Auberge du Jeu de Paume dans le Domaine même,
   musée Condé), Coupe d'Or de Polo de Deauville (palaces Barrière, L'Essentiel,
   casino et thalasso).
4. **4 voies d'invitation backfillées** : US Open Fan Week (Fan Access Pass
   gratuit qualifié, aucun contact presse nominatif publié trouvé — dit
   franchement), Polo Federations Cup Gassin (directeur du club nommé et
   sourcé via une source indépendante), Prix Jacques Le Marois et Touquet
   Classic Amateur (voir anomalie ci-dessous).
5. **Un contact halluciné intercepté avant publication** : le premier passage
   de recherche avait produit « Audrey Le Véziel — Responsable Communication,
   Événementiel et Sportif, Le Touquet Golf Resort » avec un email. Un agent
   vérificateur adversarial dédié a trouvé un profil indépendant pour ce nom
   exact rattaché à un métier totalement différent (restauration) — signal de
   fabrication ou d'homonymie. **Écarté avant publication.** Les deux autres
   noms de la même vague (Héléna Dupuy/France Galop, Charles Debruyne/Touquet)
   ont été confirmés sur le nom et la fonction par une source professionnelle
   indépendante, mais PAS sur le téléphone/email associé (jamais vu dans un
   extrait source brut) — ces coordonnées non confirmées ont été retirées ;
   seuls le nom, la fonction et les contacts génériques déjà publiés ont été
   gardés. Leçon consignée dans `lessons.md`.
6. SEO : `gen_seo.py` (ld+json, sitemap lastmod=11/08), `gen_pages.py` (472
   événements × 13 langues + hubs, sitemap 7645 URLs, 0 lien mort — la baisse
   de volume de pages vient des purges normales du plancher pendant l'absence).
7. Eyebrow déjà à jour (« 11 août 2026 ») — tenue quotidiennement par la
   passe automatique du plancher, rien à faire cette fois.

## Le reste-à-faire (recompté cette passe)
- **Traductions manquantes : 0/482.** Toujours à 100 %.
- **Séjours manquants : 263 au total, dont 42 dans la fenêtre live** (47 → 42
  après les 4 composés aujourd'hui).
- **Voies d'invitation manquantes : 167 au total, dont 6 dans la fenêtre
  live** (11 → 6... écart de 5 pour 4 backfills : la dédup a aussi retiré une
  fiche qui comptait comme manquante).
- **Guides d'accès (c=acces) : 10**, inchangé — la priorité 3 du plan du
  29/07 (écrire 10 nouveaux guides intemporels) n'a pas été engagée cette
  passe, la priorité donnée au rattrapage (dédup, purge évitée, réseau)
  après 6 jours d'absence de cette routine.
- Couverture oct-nov-déc 2026 : 74 événements, inchangée depuis le 5 août
  (aucun nouvel événement d'automne ajouté cette passe — priorité 2 du plan
  du 29/07 en attente, faute de temps après le rattrapage).

## Événements des 48 h / semaine
33 fiches démarrent dans les 7 prochains jours (11-18 août) : Monte-Carlo
Summer Festival (Lisa Stansfield le 11, Laura Pausini le 15), Gala Night de
l'Hôtel Cala di Volpe avec Katy Perry (12 août, Porto Cervo), Coupe d'Or de
Polo de Deauville (ouverture le 17), Regata Palermo-Montecarlo (départ le 18),
Fête du 15 août à Saint-Tropez/Grimaud, Prix Jacques Le Marois (16 août,
Deauville). Vérification de cohérence dates/liens faite sur cette fenêtre à
l'occasion de l'audit qui a révélé les 2 doublons — pas de lien testé en
direct cette passe (voir anomalie réseau).

## 3-5 nouveautés glamour
- Gala Night 2026 de l'Hôtel Cala di Volpe avec Katy Perry (12 août, Porto
  Cervo, Costa Smeralda).
- Regata Palermo-Montecarlo, 21e édition — désormais avec séjour Monte-Carlo
  clé en main (Le Louis XV, Yacht Club de Monaco).
- Coupe d'Or de Polo de Deauville, finale le 30 août — séjour Barrière complet.
- Chantilly Arts & Élégance Richard Mille (13 septembre) — séjour dans le
  Domaine même, à l'Auberge du Jeu de Paume.
- Dîner de gala de Ferragosto au Grand Hotel Quisisana (15 août, Capri).

## Visites (regard journaliste)
Le relevé quotidien (`stats/visites.ndjson`, tenu à jour par le plancher
pendant l'absence de cette routine) montre une **progression continue et
saine sur les 6 jours manqués** : 327 → 334 → 341 → 353 → 365 → 380 → 390
visites du 5 au 11 août, soit +19 % sur la semaine, sans rupture ni pic
suspect malgré l'absence de nouveaux contenus. Le compteur GoatCounter en
direct reste illisible depuis cette session cloud (réseau sortant bloqué,
voir anomalie ci-dessous) — même limitation que les 28-29/07 et le 05/08 ;
aucun chiffre inventé, le relevé quotidien fait foi.

## Résultats des contrôles
- `validate.py` : **OK**, 0 blocker, 0 warning.
- `perfcheck.py` : **OK**, 0 régression.
- `healthcheck.sh` : **ALERTE technique, fausse alerte connue** — http=000000
  après 10 tentatives sur 2,5 minutes. Réseau sortant bloqué depuis cette
  session cloud (confirmé dès le début de passe : `curl` direct → tunnel 403,
  `WebFetch` → `EGRESS_BLOCKED` sur constanceparis7.com **et** sur des
  domaines neutres comme wikipedia.org — seul `WebSearch` fonctionnait).
  Même anomalie documentée les 28-29/07 et le 05/08. **`rollback.sh` non
  déclenché**, à dessein (leçon établie : un 000 venu d'une session cloud est
  la sonde qui n'a pas de réseau, pas le site qui est tombé). Le contrôle qui
  fait foi reste `.github/workflows/surveillance.yml`, qui dispose du réseau.
- Étape 10 (republication de l'artifact claude.ai) : **non effectuée**, comme
  le 05/08 — `index.html` est un fichier de données brut de 2,2 Mo (12
  langues + chargeur), pas un artifact de présentation ; sans incidence sur
  le site public qui est la source de vérité.

## Anomalies (résumé)
1. **Cadence rompue : 6 jours sans passe complète** (voir en tête de
   compte rendu) — à surveiller côté ordonnanceur.
2. **Réseau sortant bloqué** pour `curl`/`WebFetch`/`healthcheck.sh` depuis
   cette session cloud — `WebSearch` fonctionnait normalement et a permis la
   recherche de fond ; aucune vérification de lien en direct (`u`) possible.
3. **1 contact halluciné intercepté et écarté avant publication** (voir
   ci-dessus) — aucune donnée fausse publiée, leçon consignée.
4. Aucune autre anomalie. Signature `radar-routine-claude` posée dès le
   début de passe ; dépôt unique (pas de dépôt privé séparé dans cet
   environnement — tout `.radar/` vit dans ce dépôt public, journaux et
   leçons poussés avec le reste).

## Auto-amélioration de la passe
- **Filet renforcé contre l'hallucination de contact** : quand `WebFetch` est
  indisponible et que la recherche ne repose que sur des résumés `WebSearch`,
  tout nom propre associé à un téléphone/email passe désormais systématiquement
  par un second agent au seul mandat de réfuter, avant publication. Un contact
  entièrement fabriqué a été intercepté ainsi cette passe. Leçon détaillée et
  règle permanente ajoutées à `lessons.md` (11/08/2026).
- **Bug de purge découvert et corrigé** : les 7 guides d'accès « intemporels »
  portaient une date d'expiration héritée d'un ancien format mensuel et
  auraient été supprimés à tort fin août. Corrigé (d2 repoussé), à surveiller
  pour tout futur guide créé (priorité 3 du plan) — s'assurer qu'un guide
  voulu intemporel ne porte pas de `d2` proche.
