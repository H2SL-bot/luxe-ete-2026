# Compte rendu — passe du 21/08/2026 (session cloud)

## Ce qui a été fait

**Chantier prioritaire : condensation des voies d'invitation — 36 fiches traitées**,
en deux lots de 18, toutes prises dans la FENÊTRE LIVE et par ordre d'imminence
(les fins de saison du 29-31/08 d'abord, puis jusqu'au 20/09).

Deux publications au fil de l'eau, chacune passée par `publier.sh` :
- lot 1 — Twiga Porto Cervo, Dolce&Gabbana × Casa Amor, Hamptons Polo, Meeting de
  Deauville, Lanterne d'Hermès (Ginza), Hôtel du Cap-Eden-Roc, Anema e Core (Capri),
  La Co(o)rniche, Casino Barrière Le Touquet, Hôtel du Palais, clubs privés de
  Mayfair, Bagni Fiore Paraggi, DaV Mare (Splendido), Covo di Nord-Est, La Gritta,
  Sottovento, JustMe Porto Cervo, Lío Ibiza ;
- lot 2 — scène yacht Ibiza-Formentera, Nammos Mykonos, Principote, Nikki Beach Miami,
  soldes de Milan, Grand Palais d'été, Grimaldi Forum, Jesus Christ Superstar
  (Marina Bay Sands), Hôtel du Palais Biarritz, Thierry Hermès (Le Forum), Phi Beach,
  Maxi Yacht Rolex Cup, Nikki Beach Saint-Tropez, Cannes Yachting Festival,
  L'Heure Dorée (Peninsula), Luisa Spagnoli × Da Luigi, dîner Ayla Privé,
  WE ARE [still] HERE (Petit Palais).

**Effet mesuré sur le filet** (compteurs `validate.py`, avant → après) :
- `iv.g` au-dessus de 1 200 car. : 90 → 68 fiches ; excédent 65 785 → 50 778 car.
- `iv.w` au-dessus de 1 200 car. : 110 → 87 fiches ; excédent 104 952 → 81 244 car.
- soit ~38 700 caractères de journal d'enquête retirés des pages visiteur.

**Reste à condenser : 97 fiches, dont 70 dans la fenêtre live.**

## Contrôle de non-perte de faits (obligatoire, jamais sur parole d'agent)

`verif_faits.py` a été passé sur les deux lots. 12 alertes au total :
- **4 pertes réelles, corrigées à la main avant publication** — une adresse de service
  déformée (`press@` au lieu de `presse@butler-collection.fr`), une URL SevenRooms
  abrégée en « .../paraggifiore », la page tarifaire `sottoventoclub.com/prenota-pista-2/`
  et deux URL Hermès informatives, toutes réinjectées.
- **8 fausses alertes de format ou suppressions légitimes**, vérifiées une par une :
  un horodatage machine `data-date="1786406340"` lu comme un téléphone ; une URL
  comptée perdue parce que le sous-domaine `billetterie.` avait changé la
  normalisation ; un « 15 € d'économie » qui est un calcul, pas un tarif publié ;
  et surtout des données que la fiche elle-même déclarait **périmées ou non
  officielles** — `reservations.miami@nikkibeach.com` et le (305) 538-1111 signalés
  périmés par la source, les « 85 $ » de brunch et « 200 $ » de daybed venant de
  plateformes tierces et non de Nikki Beach. Les republier aurait été une faute :
  leur retrait est conforme.

**Protection des personnes** : trois fiches portaient encore des coordonnées
nominatives, retirées à cette occasion — un e-mail nominatif chez Butler Collection,
un mobile non confirmé attribué à une personne chez Principote, et les mobiles
personnels des trois attachées de presse de Zmirov Communication sur le Cannes
Yachting Festival. Dans les trois cas le NOM et la FONCTION sont conservés, ainsi
que la boîte de service (`yachtingcannes@zmirov.com`) : aucune fiche n'a perdu sa
porte d'entrée.

## État du site

- 430 événements ; fenêtre live 306 fiches ; 93 dans les 90 jours.
- **LOI DU SITE honorée à 100 % sur la fenêtre live** : 0 fiche sans séjour
  (hors dossiers d'accès), 0 fiche sans voie d'invitation. Les 63 séjours et
  17 invitations que `reste.py` annonce manquants portent tous sur des
  événements DÉJÀ PASSÉS, conservés 30 jours avant purge.
- Traductions : 430/430 (100 %).
- KPI accès mondain : 291/296 (98 %).
- `validate.py` : 0 blocage, 2 avertissements (les deux compteurs de condensation
  ci-dessus, en baisse). `perfcheck.py` : 0 régression. `healthcheck.sh` : http 200,
  date fraîche, 430 servis = 430 attendus.

## Rien de neuf n'a été ajouté au radar

Aucun événement nouveau ce jour : la consigne place la condensation avant la
recherche de nouveautés, et les deux lots ont occupé la passe. C'est un choix
assumé, pas un échec de recherche.

## Ce que je n'ai PAS pu faire ou vérifier

1. **L'artifact Claude n'a pas pu être republié.** L'outil répond que la page est
   introuvable ou n'est plus partagée avec cette session
   (`artifact not found`, sur l'URL 89b85688-…). La doctrine (étape 10) demande cette
   republication à chaque passe : elle est en échec et le restera tant que
   l'artifact n'aura pas été repartagé ou recréé. **Sans conséquence pour le public** :
   la seule adresse vivante qui compte, constanceparis7.com, est à jour et saine.
2. **Aucune vérification en ligne des liens ni des sources** n'a été tentée cette
   passe : le travail était purement rédactionnel, sur des faits déjà vérifiés et
   déjà présents dans les fiches. Aucun fait nouveau n'a donc été introduit, et
   aucun n'avait besoin d'être confirmé au réseau.
3. **La joaillerie reste le trou du radar** : 2 fiches seulement en fenêtre live
   (les deux expositions parisiennes, Van Cleef & Arpels et Daniel Brush), contre
   les 10 que demande la doctrine. Aucun lancement de collection, aucune vente,
   aucun salon. C'est le chantier à ouvrir à la prochaine passe, avant tout autre
   ajout — pistes déjà datées dans la doctrine : Sotheby's Genève (30/10-13/11/2026),
   Watches and Wonders (5-11/04/2027), GemGenève (11-14/05/2027).
4. **Le piège du « 31 août »** n'a pas été traité : des fiches portent encore une
   fin de saison au 31/08 qui est un bouchon, pas une date vérifiée. Elles vont
   disparaître de l'écran le 1er septembre, la plupart à tort. **C'est urgent :
   il reste dix jours.**

## Anomalie de déclenchement

`precheck.sh` a signalé une **CADENCE ROMPUE : 39 h depuis le dernier run
journalisé** (seuil 30 h). Une passe a donc été manquée. Celle-ci a été menée en
rattrapage complet. Le push direct sur `main` a fonctionné — aucun repli sur une
branche `claude/*` n'a été nécessaire.

## Visites

1 817 visites aujourd'hui, contre 1 795 hier et 1 711 avant-hier : la progression
se poursuit, plus lentement, après le bond du 19 août (1 046 → 1 711 en une nuit,
soit +64 %). Le palier des 1 800 est franchi pour la première fois. Le détail par
pays, par page et par source n'est pas lisible depuis cette session (le tableau
GoatCounter demande le réseau) : je ne peux donc pas dire cette fois quelles fiches
attirent ni d'où viennent les visiteurs, et je préfère le dire plutôt que de
l'inventer.
