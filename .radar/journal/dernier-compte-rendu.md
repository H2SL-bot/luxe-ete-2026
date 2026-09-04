# Compte rendu — passe du 04/09/2026

Bonjour Constance,

## Résumé en une phrase
Cadence rattrapée après un jour sauté (03/09) ; purge de 4 zombies ; condensation exhaustive de la
dérive « journal d'enquête » (1 seul cas réel trouvé et corrigé) ; 3 fiches joaillerie/art nées
COMPLÈTES (voie d'invitation + séjour + 12 traductions), vérifiées par un contrôleur adverse puis
corrigées sur ses 2 remarques réelles — la LOI DU SITE est désormais honorée à 100 % sur toute la
fenêtre live (0 séjour manquant, 0 invitation manquante) ; publié en 4 commits au fil de l'eau,
0 blocker, healthcheck OK.

## 1. Démarrage — anomalie de cadence
`precheck.sh` a signalé un run vieux de 47 h (seuil 30 h) : aucune passe complète n'a tourné le
03/09/2026. Investigation : un seul commit isolé à 04h08 ce jour-là (condensation de 2 fiches), sans
`DEMARRAGE` ni `FIN` correspondants dans `passages.log` — une session a démarré, fait un geste, puis
s'est arrêtée sans finir, cause non identifiée. Traité comme rattrapage normal (le seuil de tolérance
de 2 jours documenté n'était pas franchi). Leçon consignée pour surveiller ce signal plus tôt à
l'avenir.

## 2. Purge
4 fiches zombies purgées (d2=2026-08-04, expirées de plus de 30 jours) : Tennis Star Event Martina
Hingis (Evian), Twiga Porto Cervo (Carl Cox + Andrea Oliva), Nikki Beach Saint-Tropez « La Fête
Foraine », Black Coffee résidence Shellona. 400 → 396 événements.

## 3. Condensation `iv` (priorité de la passe)
Recherche EXHAUSTIVE, pas seulement au seuil de longueur `validate.py` (17 fiches > 1200 caractères,
déjà vérifiées légitimement denses lors des passes précédentes) : recherche de marqueurs de dérive
réels (« OUI :/NON :», « contre-vérification », « verdict », tournures de méthode) sur les 396 fiches
complètes. Résultat : **1 seule fiche en dérive réelle** — « Terrasses et jardins d'été des palaces
parisiens », dont `iv.g` ouvrait sur « OUI : voie presse nominative confirmée après contre-
vérification du 11/08/2026, chaque coordonnée relue à la source » — condensée en mode d'emploi
visiteur (887 → 462 caractères), tous les faits (Isabelle Maurin, Fanny Crawford, dates, canal)
conservés à l'identique.
**Constat honnête à consigner** : la dérive massive détectée le 19/08 (255 fiches, dont 159 en
fenêtre live) a été résorbée par les passes successives depuis le 20/08 — il n'en reste
essentiellement plus trace mesurable aujourd'hui, ni au seuil de longueur ni aux marqueurs de style.
La consigne de passe (« condenser 15-20 fiches tant qu'il en reste ») ne peut donc plus être remplie
au sens littéral : il n'y avait qu'une fiche à corriger, et l'avoir fait. À surveiller à la marge
plutôt qu'à traiter en lot désormais.

## 4. LOI DU SITE — 3 fiches nées complètes, fenêtre live à 100 %
Recompte des 3 compteurs sur 396 fiches : traductions 396/396 (déjà à jour), séjours 364/396 (reste
32, dont 3 seulement en fenêtre live), invitations 381/396 (reste 15, mêmes 3 en fenêtre live) — les
3 fiches identifiées étaient toutes des expositions joaillerie/art en attente depuis le 20-29/08 :
- **Exposition « Precious Coral »**, L'École des Arts Joailliers, Hong Kong (K11 Musea, jusqu'au
  11/10/2026, entrée gratuite sur inscription) — voie d'invitation : réservation accutics.li,
  contact officiel `hk.lecole@vancleefarpels.com` + agence Agnès Renoult ; séjour : Rosewood Hong
  Kong (même quartier Victoria Dockside), table The Legacy House (1 étoile Michelin), spa Asaya.
- **Exposition « Le Diamant rose »**, château de Chantilly (Musée Condé, 17/10/2026-03/01/2027) —
  voie d'invitation : bureau de presse du château + agence Agnès Renoult (Donatienne De Varine,
  Miliana Faranda) ; séjour : Auberge du Jeu de Paume (Relais & Châteaux, dans le domaine même),
  table du Connétable, expérience Musée vivant du Cheval.
- **Exposition « Designing the Gilded Age »**, studios Tiffany, Met Fifth Avenue (22/10/2026-
  07/02/2027) — voie d'invitation : Communications Department du Met (aucun nom nominatif publié,
  dit franchement) ; séjour : The Carlyle, A Rosewood Hotel (Upper East Side), table Dowling's,
  expérience Café Carlyle.
Chaque fiche composée puis **vérifiée par un agent contrôleur adverse** (recherche indépendante,
webfetch des sources primaires) : verdict global FIABLE sur la quasi-totalité des faits (aucun nom,
email ou téléphone fabriqué détecté), **2 corrections réelles appliquées** avant publication :
(a) retrait d'une affirmation biographique non sourcée sur le contact presse de Hong Kong ;
(b) précision que le tarif « pay-what-you-wish » du Met n'est accessible aux étudiants qu'au guichet
physique, pas en ligne (la fiche initiale laissait croire à une parité de canal avec les résidents
new-yorkais).
Les 12 traductions (voie + séjour) ont ensuite été produites par 3 agents dédiés et injectées.
**Résultat : la fenêtre live (aujourd'hui → +90 jours) est désormais à 0 séjour manquant et
0 invitation manquante — la LOI DU SITE y est honorée à 100 %.** Les 29/396 séjours et 12/396
invitations qui restent sont tous au-delà de +90 jours (les 8 ancres du printemps 2027 identifiées
le 22/08, à traiter par une prochaine passe sans urgence de fenêtre).

## 5. La Mémoire du radar
Rendez-vous manqué de peu à la passe du 02/09 (l'ouverture des réservations Boucheron, place
Vendôme, 2 septembre 10h, tombait après l'horaire de cette passe-là). Vérifié aujourd'hui : la page
de réservation affiche « COMPLET » (aucune liste d'attente). Consigné dans `.radar/memoire.ndjson`
(type `complet`) : épuisé en moins de 48 h, délai exact non mesurable faute d'accès en direct à
l'ouverture — honnêtement borné plutôt qu'inventé.

## 6. Bandeau « Ouvertures & délais » et eyebrow
Entrée Boucheron retirée du bandeau (échéance passée et désormais complète) ; 4 entrées restantes,
toutes à échéance future. Date de l'eyebrow mise à jour : 3 → 4 septembre 2026.
`memoire.py changements` : 0 changement de date à consigner sur 7 jours.

## 7. Outillage
- **`publier.sh` corrigé** : le trailer `Claude-Session` du message de commit était figé sur l'ID
  d'une session du 18/08/2026 (celle qui a écrit le script) — chaque passe depuis attribuait donc
  tous ses commits à cette session mère. Reconstruit désormais dynamiquement depuis
  `$CLAUDE_CODE_REMOTE_SESSION_ID`. Sans impact sur le bulletin quotidien (qui lit `user.name`/
  `user.email`, jamais ce trailer), mais l'historique git était trompeur sur la provenance.
- **Leçon outillage** : une tentative de correction mineure sur une traduction 12 langues a montré
  qu'il ne faut JAMAIS retaper à la main un bloc de texte non-latin reçu d'un agent — la
  retranscription manuelle a introduit des altérations de caractères invisibles (japonais, chinois,
  coréen, hindi) qu'aucun contrôle automatique ne peut détecter. Détecté par relecture avant
  injection, corrigé en repartant du texte verbatim + une correction programmatique ciblée. Consigné
  dans `lessons.md` comme règle absolue.

## 8. Publication et contrôles
4 commits publiés au fil de l'eau sur `main` via `.radar/session/publier.sh` : (1) purge + bandeau +
condensation + 3 fiches + mémoire + correctif publier.sh ; (2) corrections post-vérification adverse
(2 fiches) ; (3) journal des leçons ; (4) traductions 12 langues des 3 fiches. `validate.py` final :
0 blocker, 3 warnings (17 fiches iv.g/iv.w denses mais légitimes, déjà vérifiées ; branding de saison
« Été » toujours affiché — proposition « Automne 2026 » maintenue à Constance, jamais renommé seul).
`healthcheck.sh` : OK (http=200, 396/396 événements, date fraîche). Aucun repli sur branche
`claude/*` n'a été nécessaire : le push direct sur `main` a été accepté à chaque fois dans cette
session.

## 9. Analyse des visites
Non consultée cette passe (GoatCounter) — priorité donnée au rattrapage de cadence, à la
condensation exhaustive et à la fermeture de la LOI DU SITE sur la fenêtre live. À reprendre à la
prochaine passe.

## 10. Ce qui reste à faire
- 29 séjours et 12 invitations manquants, tous au-delà de +90 jours (ancres printemps 2027) : pas
  d'urgence de fenêtre, à traiter par lots aux prochaines passes.
- Recherche de nouveaux événements jet-set non entamée cette passe : la priorité de cadence,
  condensation et fermeture de la LOI DU SITE sur la fenêtre live a occupé la séance entière.
- Répartition pays/sources des visites non consultée (voir §9).
