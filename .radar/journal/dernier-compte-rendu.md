# Compte rendu — passe du 29/08/2026

Bonjour Gérald,

## Résumé en une phrase
Passe complète : purge de 4 fiches zombies, condensation de 20 fiches (dérive « journal
d'enquête » → mode d'emploi visiteur), et 13 fiches joaillerie nées incomplètes le 20/08
sont désormais complètes (voie d'invitation + séjour clé en main), recherche réelle et
vérification adversariale à chaque étape.

## 1. Purge
4 fiches zombies purgées (d2 antérieur à aujourd'hui-30j, non purgées automatiquement) :
La Réserve à la Plage (soirées brasero), Festival de Saint-Paul-de-Vence 15e édition,
Expositions du Lavoir Vasserot, Polo Parade. 435 → 431 événements.

## 2. Condensation de la dérive « journal d'enquête » (priorité de la passe)
20 fiches de la fenêtre live condensées (les plus imminentes d'abord, du 13/09 au 22/11) :
iv.o/iv.g/iv.w réécrits en mode d'emploi visiteur, tournures d'enquêteur et titres de
section retirés, tous les faits durs conservés à l'identique. Contrôle mécanique
`verif_faits.py` passé sur les 20 fiches : 7 alertes initiales, 5 vraies pertes corrigées
(fourchettes de prix compressées sans le €, détail de tarif plage, URL alias manquante,
formulation d'année collée au prix), 2 exclusions légitimes confirmées (adresse et URL
explicitement signalées erronées par le texte source lui-même).
Compteurs `validate.py` : iv.g 33 → 29 fiches au-dessus du seuil, iv.w 58 → 48.
Reste 29 (iv.g) + 48 (iv.w) fiches à condenser aux prochaines passes.

## 3. LOI DU SITE — 13 fiches joaillerie nées complètes aujourd'hui
Constat de la passe : les 14 fiches joaillerie créées le 20/08 (place Vendôme JEP/Journées
Particulières LVMH, expositions Van Cleef & Arpels Vienne, Cartier Melbourne, Doha
Jewellery, Mikimoto Osaka, ventes Christie's/Sotheby's/Phillips Genève) étaient toutes
nées SANS séjour ni invitation — une violation de la LOI DU SITE passée inaperçue.
13 des 14 ont été recherchées, composées puis vérifiées par un contrôleur adverse dédié
(séjour et invitation séparément, 1 agent par fiche et par étape) :
- **Séjours** : 13/14 fiables (hôtels, tables, expériences réels, vérifiés de première
  main). La 14e (« Precious Coral » Hong Kong, fiche 408) a été jugée à tort fiable=false
  par son vérificateur — voir section 4.
- **Invitations** : 13/13 composées et vérifiées ; garde-fou RGPD appliqué strictement à
  chaque étape (plusieurs contacts nominatifs et mobiles personnels trouvés en cours de
  vérification ont été volontairement écartés, seules les voies de service publiées).
  Un lien de billetterie (universe.com, fiche Boucheron) a été détecté comme un HTTP 200
  trompeur (page vide quel que soit l'identifiant testé) et retiré.

Séjours clé en main : 361 → 374 (reste 57, dont probablement peu en fenêtre live).
Voies d'invitation : 398 → 411 (reste 20).
KPI ACCÈS mondain (iv) : 92 % → 96 % (284/293 fiches mondaines de la fenêtre live).

## 4. La fiche 408 n'a pas été retirée — le vérificateur avait cherché au mauvais endroit
Le contrôleur adverse du séjour 408 (« Precious Coral », L'École des Arts Joailliers, Hong
Kong) a conclu à tort que l'exposition n'existait pas pour 2026, faute de la trouver sur le
hub global de la maison. Avant de retirer l'événement, j'ai retesté l'URL `so` déjà
enregistrée dans la fiche (`lecolevancleefarpels.com/hk/en/exhibition/...`, sous-site
Hong Kong) : elle charge parfaitement et confirme les dates exactes (23 mai → 11 octobre
2026). L'événement est réel et reste en ligne. Leçon consignée dans `tools/lessons.md`
(vérifier l'URL déjà enregistrée, pas seulement le hub global, pour les maisons à
microsites régionaux). **Reste à faire à la prochaine passe** : composer et vérifier le
séjour + l'invitation de la fiche 408 en ciblant directement ce sous-site.

## 5. Traductions
431/431 fiches traduites dans les 13 langues — 0 manquante.

## 6. Ce qui n'a pas pu être vérifié / signalé sans agir
- 6 nouvelles fiches (les invitations joaillerie composées aujourd'hui) ont un `iv.o` ou
  dépassent le seuil WARN de 1200 caractères — à condenser à une prochaine passe (la plus
  longue : Christie's Genève, 2307 car.).
- La date d'ouverture des réservations Boucheron JEP (« 2 septembre 10h ») trouvée par
  l'agent de recherche n'a pas pu être confirmée indépendamment par le vérificateur — non
  ajoutée au bandeau « Ouvertures & Délais » par prudence (source unique, non recoupée).
- Branding de saison : « Été » toujours affiché au 29/08. Proposition à Gérald : passer à
  « Automne 2026 » (jamais renommé sans son accord).
- Fiche 408 : reste sans séjour ni invitation (voir section 4).

## 7. Publication et contrôles
`validate.py` : 0 blocker, 4 warnings (iv.o/iv.g/iv.w journal d'enquête résiduel + branding
saison) à chaque étape avant publication. 4 commits publiés au fil de l'eau (purge,
condensation, séjours, invitations). `healthcheck.sh` : OK (http=200, 431/431 événements,
date fraîche).

## 8. Réseau
`WebSearch` épuisé (200/200) après les premières recherches de séjours/invitations ; bascule
systématique des agents sur `WebFetch`/`curl` direct sur les sites officiels pour la suite de
la passe — signalé par la quasi-totalité des agents de recherche/vérification tardifs.
