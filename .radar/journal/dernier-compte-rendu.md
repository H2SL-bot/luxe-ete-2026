# Compte rendu — passe du 28 juillet 2026 (cloud, radar-routine-claude)

## État général
- validate.py : OK — 0 blocker, 0 warning. 470 événements, 152 dans la fenêtre
  [aujourd'hui..+90j], traductions 470/470 (100%).
- perfcheck.py : OK — 0 régression (+0,00 Mo, +0 événement). Index allégé
  0,40 Mo gzip, 12 langues différées servies par i18n-data/.
- KPI ACCÈS mondain (iv) : 191/351 (54%).
- Purge : 0 fiche à purger (aucun d2 < aujourd'hui−30j).
- Adresse publique https://constanceparis7.com : à jour (poussé sur main),
  eyebrow « 28 juillet 2026 ». Artifact republié (V2-maj-28-07).

## Fait pendant la passe
1. Backfill « promesse d'accès » : 12 fiches prioritaires (Monaco Yacht Show,
   Arc de Triomphe, Summer Party Southampton, Soirée Blanche Megève, Hampton
   Classic, Cap-Ferrat, SOUL! Monte-Carlo, Polo Deauville, Ramatuelle,
   Portofino, Délices Sonores, Besch Cannes Auction) — iv_o/iv_g/iv_w traduits
   et injectés en 6 langues : en, es, pt, ar, zh, ja (216 valeurs).
2. Fusion du chantier « mesure d'audience » poussé par Gérald pendant la passe
   (voir Anomalies) : pages fiches régénérées avec le nouveau gabarit — le
   mouchard GoatCounter est bien présent sur les 456 pages.
3. SEO : sitemap.xml lastmod=2026-07-28, ld+json 60 événements, 6172 URLs.
4. Filet renforcé : gen_seo.py refuse désormais un argument non-date
   (leçon du jour — un « --help » était parti dans le sitemap, corrigé).
5. Vérification des événements des 7 prochains jours par recherche web :
   dates confirmées pour Délices Sonores (5/08, Citadelle, 40-50 €, line-up
   Matt Sassari), Nikki Beach « La Fête Foraine » by Perrier-Jouët (4/08),
   feu d'artifice pyromélodique Monaco (1/08, Port Hercule + Jardin Exotique
   sur réservation SMS), Starlite Marbella (saison jusqu'au 29/08).

## Backlog
- SOLDÉ LE JOUR MÊME (demande expresse de Gérald, ~15h30 UTC) : le backfill iv
  en it/de/ru/ko/hi/tr a été repris après le reset du quota et publié — les
  12 fiches prioritaires sont désormais complètes dans les 12 langues
  (390 valeurs iv_o/iv_g/iv_w au total sur la journée). validate/perfcheck
  re-passés au vert, site et artifact republiés.
- PUIS, 2e demande expresse de Gérald (~17h UTC) : les 24 dernières fiches ont
  été traitées dans la foulée (5 agents, 10 langues manquantes, 720 valeurs).
  RÉSULTAT : plus AUCUNE fiche du site avec un accès iv non traduit —
  la promesse d'accès est couverte à 100% dans les 12 langues.
  Au passage, fusion des chantiers poussés par Gérald pendant le travail
  (voile d'affichage des événements terminés, relevé visites, cron 5h55) ;
  les pages et l'index ont été régénérés sur cette base fusionnée.

## Événements des 48 h
- 29/07 : Polo Parade sur le vieux port (Saint-Tropez) ; SOUL! An Exclusive
  Show, Salle des Étoiles (29-30/07 puis 3-9/08).
- 30/07 : Jumping International de Dinard CSI 5*.
- 28/07-01/08 : Qatar Goodwood Festival « Glorious Goodwood ».

## 3-5 nouveautés glamour (fenêtre proche)
- SOUL! — dîner-spectacle exclusif SBM, dès ~260 €, accréditation presse possible.
- La Fête Foraine by Perrier-Jouët à Nikki Beach (4/08).
- Black Coffee en résidence à Shellona (4/08, Ramatuelle).
- Délices Sonores à la Citadelle de Saint-Tropez (5/08), salon VIP réservable.
- BIG ART Festival avec Robbie Williams au Romazzino Belmond (9/08).

## Visites (regard journaliste)
Premier relevé du compteur public : 113 visites cumulées au 28 juillet — c'est
le point zéro de la mesure, pas encore de progression à commenter. Le fait
marquant est ailleurs : le mouchard vient d'être étendu aux 456 pages fiches,
jusqu'ici invisibles du compteur ; dès demain, on saura enfin quelles fiches
attirent les arrivées Google directes. Tableau public :
https://constanceparis7.com/tableau-de-bord.html

## Anomalies
1. CADENCE ROMPUE (precheck) : dernier run journalisé il y a 146 h. Les passes
   des 23-27/07 ont été assurées par le plancher GitHub Actions (commits
   radar-passe-quotidienne quotidiens) mais AUCUNE routine Claude n'a tourné
   depuis le 22/07 — cette passe est donc une passe de rattrapage. Le
   déclenchement de la routine à 7h03 ne s'est pas produit 6 jours de suite ;
   la présente exécution est arrivée à ~12h35 UTC. À surveiller demain.
2. Réseau sortant : la politique d'egress de l'environnement bloque les
   requêtes directes (curl → 403 proxy) vers les sites des événements. Le
   test des liens `u` en HTTP direct est impossible depuis cette session ;
   la vérification des liens reste assurée par le plancher quotidien
   (passe_automatique.py, dernier passage 28/07 10:32). Les vérifications de
   contenu ont été faites via la recherche web.
3. Limite de session atteinte en cours de passe (cf. Backlog).
4. Push concurrent : deux commits (relevé de visites, mouchard fiches) poussés
   par Gérald pendant la passe → fusion propre, pages régénérées avec le
   nouveau gabarit, rien perdu des deux côtés.
5. healthcheck.sh post-publication : http=000000 — la sonde n'a PAS de réseau
   depuis cette session (même blocage qu'en 2.), ce n'est pas un site KO.
   Pas de rollback (il aurait été injustifié) : le plancher a vérifié le site
   en ligne à 10:32 UTC (200, 470 événements, date fraîche) et le workflow
   surveillance.yml refera un contrôle réseau vers 18h23 Paris — il ouvrira
   une issue si la publication de cette passe n'était pas servie.
