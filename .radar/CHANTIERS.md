# LES CHANTIERS DE CONSTANCE — ce qui reste à faire sans toucher au code

État mesuré le **20/08/2026 au soir**. Chaque chiffre a été compté sur le site
en ligne, pas estimé. À tenir à jour : ce document existe parce que la première
version de cette liste n'était nulle part et s'est perdue.

À distinguer du `RESTE-À-FAIRE` de la DOCTRINE, qui est le plan **éditorial** de
Gérald (traductions, automne, guides d'accès). Ici : ce que Constance peut
décider et faire faire, sans écrire une ligne de code.

---

## ✅ RÉGLÉS LE 20/08/2026

**01 · Sept pages qui appartenaient à un tiers** — copies brutes du site Groot
Hospitality / LIV Nightclub, en ligne depuis le 11/08. Vérifié sur les 6 978
pages : zéro lien entrant, absentes du sitemap, aucune fiche ne s'en servait.
Supprimées, les sept répondent 404.

**02 · 610 personnes joignables depuis le site** — 629 coordonnées nominatives
retirées (e-mails, portables, lignes directes) sur 129 fiches, français et 12
langues. Conservés : noms, fonctions, et toutes les voies de service. Archivées
en privé dans le coffre Obsidian. Règle inscrite dans la doctrine, outils
`.radar/tools/contacts_*.py`.

**03 · Mentions légales** — obligation de l'article 6 de la LCEN, absentes.
Publiées : `/mentions-legales.html`. Régime « éditeur non professionnel » :
l'adresse postale n'est pas publiée. Directeur de la publication : Gerald
Lefebvre jusqu'au 21/09/2026, puis bascule automatique sur Constance.

**04 · À propos et contact** — inexistants. Publiés : `/a-propos.html`, liés
depuis toutes les pages ET depuis le haut de la page d'accueil. Contient la
clause d'indépendance : « une place dans le radar ne s'achète pas ».

---

## ✅ RÉGLÉ LE 24/08/2026

**15 · Les guides d'accès : les 6 existent**
Accréditation presse (145 fiches desservies, écrit le 21/08 par la passe), puis
le 24/08 : agences de relations presse (82), listes d'invités et RSVP (99),
tables réputées impossibles (123), vernissages et previews (40), tirages au
sort (8 fiches en parlent, 3 seulement le pratiquent : dit honnêtement).
Rédigés depuis le corpus des fiches du radar, zéro exemple inventé
(vérification mécanique : 0 introuvable), contre-lecture indépendante ; le
guide des tirages a reçu une contre-lecture manuelle finale, sa traduction
`ds` retirée des 12 langues (repli français, règle de cohérence). Publiés en
13 langues, 444 fiches en ligne. S'ajoute `llms.txt`, carte du site pour les
assistants IA (38 visites venues de ChatGPT en un mois).

## 🔄 EN COURS

**05 · 147 fiches à re-vérifier** → **120 restantes**
Fiches contrôlées sans accès web : la page officielle lue, mais rien pour la
contredire. 27 reprises le 20/08 : 12 tranchées, 12 dates corrigées, 1 doublon
retiré, le reste inscrit avec sa preuve.
**Découverte majeure** : 46 fiches portaient le 31/08 en date de fin — une
valeur par défaut, pas une information. 11 établies à leur source, **aucune
n'était juste**. 22 restent, dont l'établissement ne publie rien : elles ne se
règleront que par courriel. 6 lettres partent le 21 et le 24 août.
→ voir `.radar/a-reverifier.md`

---

## ⬜ À FAIRE

**06 · ~~La page d'accueil est illisible sans JavaScript~~ → RÉGLÉ le 20/08/2026,
mais pas pour la raison annoncée.**

Le constat initial était EXAGÉRÉ, et il faut le dire : mesures relevées le
20/08 — chargement complet en **0,52 s**, 1,05 Mo transférés, **3 ressources
externes** seulement. Un robot sans JavaScript reçoit déjà **60 événements
structurés** en ld+json, plus la description et les balises og complètes. La
peur « Google ne voit rien » était infondée.

**Mais le diagnostic a trouvé un vrai défaut, invisible jusque-là :** la racine
était **la seule page du site sans aucune balise hreflang**, quand les 12
accueils de langue et les 6 971 pages générées en déclarent 14. Or Google
n'honore une déclaration hreflang que si elle est RÉCIPROQUE : le groupe des 13
langues risquait d'être ignoré en entier. Corrigé — 14 balises posées, diff
vérifié (14 lignes ajoutées, 0 retirée), réciprocité établie en ligne.

**Non fait, délibérément :** découper le bloc de données (90 % du poids).
Opérer le cœur de l'application pour gagner sur une page qui charge en une
demi-seconde n'est pas justifié tant que les chantiers 12 et 07 sont ouverts.

**07 · ~~La joaillerie est absente~~ → RÉGLÉ le 23-24/08/2026**

Constance a donné le cap : « les maisons de la place Vendôme ». Chasse à
8 chercheurs (un par maison ou groupe), chaque piste datée contre-vérifiée sur
sources ouvertes. **16 pistes confirmées, 0 rejetée, 43 impasses consignées**
(rien de daté chez Piaget, Chopard, Messika, Buccellati, Mellerio, Bulgari
hors Biennale : dit honnêtement plutôt qu'inventé).

**Joaillerie : 5 → 18 fiches**, publiées le 24/08 avec leurs 12 traductions
(1 056 chaînes). Les temps forts : Boucheron ouvre le 26 place Vendôme aux
Journées du Patrimoine (19-20/09, résa le 02/09 à 10h, à annoncer sur
Instagram la veille) ; Chaumet au 12 et Repossi au 6 pour les Journées
Particulières LVMH (16-18/10) ; L'École des Arts Joailliers à
Mercy-Argenteau, Chantilly (« Le Diamant rose », 17/10 → 03/01/27) et
Hong Kong ; Van Cleef & Arpels au MAK de Vienne ; Cartier au NGV de
Melbourne ; Doha Jewellery and Watches Exhibition ; et la semaine des joyaux
de Genève en novembre (Christie's, Sotheby's ×2, Phillips), expositions
publiques des lots comprises. Plus 2 fiches art (studios Tiffany au Met,
Vermeer à Osaka sous mécénat Mikimoto).

Deux pièges de dates désamorcés en chemin : la fin du NGV est le 04/10 (pas
le 23/08 recopié par des agendas) et Chantilly ferme le 03/01 (pas le 21/02).
Toutes les dates de fin ont été LUES sur la source, aucune posée par défaut.

Reste ouvert, plus petit : les 3 anciennes fiches joaillerie à dates
inventées (Chaumet Ion Orchard, Hublot, Swatch : « 01/07 → 31/07 ») sont
à re-vérifier via le chantier 05.


**08 · ~~Le radar s'éteint au printemps 2027~~ → SOCLE POSÉ le 24/08/2026**

Les 8 ancres de la doctrine sont vérifiées et en ligne en 13 langues :
TEFAF (13-18/03, previews 11-12), Watches and Wonders (05-11/04, week-end
public porté à 3 jours), Salone del Mobile 65e + Fuorisalone (avril, deux
fiches légitimes), Cannes 80e (11-22/05), GemGenève (11-14/05), Grand Prix
de Monaco 84e (03-06/06, publié AVEC la mention « sous réserve FIA »
maintenue par l'ACM, consigne acm.mc respectée, seconde expertise), Royal
Ascot (15-19/06). Avril 2027 : 0 → 3 fiches. Reste l'ÉLARGISSEMENT
(Fashion Weeks AH 27-28, Bal de la Rose, Chelsea Flower Show, Le Mans,
Art Basel Bâle...) : une par passe, consigne inchangée dans la doctrine.


**09 · Les 13 langues n'ont jamais été relues par un humain**
433 fiches × 12 langues traduites automatiquement. Personne n'a lu l'arabe, le
japonais, le hindi. Une seule tournure ridicule dans une langue, et le site perd
sa crédibilité auprès de ce public — sans que personne ne le signale jamais.
Priorité : les 12 accueils de langue, ce sont les pages vues en premier.

**10 · ~~Neuf doublons possibles nom + ville~~ → RÉGLÉ le 22/08/2026**

Le relevé a trouvé **sept** paires, pas neuf. **Quatre étaient de fausses
alertes** : Art Basel et Art Central à Hong Kong, Airelles et Cheval Blanc à
Courchevel, le Bal et le Concert du Nouvel An des Wiener Philharmoniker,
Sottovento et JustMe à Porto Cervo. Deux noms proches, deux événements réels.

**Trois étaient de vrais doublons**, tranchés après lecture des sources
officielles et contre-expertise adversariale (deux avocats du maintien par
paire, angle éditorial et angle factuel) : les trois ont conclu « fusionner »,
aucune réfutation. 430 → 427 fiches.

- **Qatar Prix de l'Arc de Triomphe** : les deux fiches ne se ressemblaient
  pas, elles pointaient LA MÊME page de billetterie France Galop, en français
  et en anglais. Conservée la version française ; greffées l'adresse postale
  complète et la mention des prestataires d'hospitalité tiers (Racing Breaks),
  qui ne figure que sur la page anglaise et aurait été perdue.

- **Grand Palais d'été** : deux photographies d'une seule saison, prises à deux
  moments. Celle qui portait une fin au 26 juillet aurait fait disparaître du
  radar une saison ouverte jusqu'au 6 septembre. Fusionnée en « Grand Palais
  d'été, édition 2026 » (02/06 → 06/09), avec sa vraie structure en deux temps :
  spectacles et After Nef jusqu'au 18 juillet, installations de la Nef jusqu'au
  26, puis Leandro Erlich seul jusqu'au 6 septembre. **La contre-expertise a
  rattrapé une erreur que j'allais commettre** : Hilma af Klint n'est pas un
  volet de la saison estivale mais une exposition distincte, coproduite avec le
  Centre Pompidou, en galerie 8 jusqu'au 30 août.

- **Les Grimaldines** : une seule 23e édition, en quatre mardis. La fiche
  « soirées d'août » n'était pas un événement, c'était la seconde moitié de
  l'autre, découpée arbitrairement, même URL et même billetterie. Fusionnée en
  « Les Grimaldines, 23e édition », les quatre soirées au même rang.

**Deux fiches renommées, donc deux anciennes adresses de page perdues** : leurs
libellés annonçaient un mois qui ne les décrivait plus. Coût assumé et consigné.

**Les 12 traductions ont été refaites** pour les deux fiches réécrites, 96
chaînes : corriger le français sans les traductions aurait recréé la
« divergence muette » de l'incident du 12/08.

validate 0 bloqueur · perfcheck 0 régression · sitemap 6 866 URLs, 0 lien mort
· healthcheck http=200, 427 fiches en ligne · aucune date modifiée ailleurs.


**11 · ~~Le nom de domaine n'est pas verrouillé~~ → DÉJÀ FAIT, constaté le 21/08/2026**

Vérifié au registre : `constanceparis7.com` porte le statut
**`clientTransferProhibited`**. Le verrou de transfert est ACTIF — personne ne
peut déplacer le domaine sans autorisation explicite. Gandi l'applique par
défaut.

Ce chantier n'aurait pas dû figurer au plan : je l'y avais inscrit sans le
vérifier. Rien à faire.

**12 · Il n'existe aucune lettre d'information** — *décidé le 21/08/2026 : ouverture le 21 septembre, à la majorité. Forme retenue : hebdomadaire du vendredi, centrée sur les délais des voies d'entrée. Détail complet dans la doctrine, section « BASCULE DATÉE ».*
Vérifié : **zéro formulaire, zéro champ e-mail** sur tout le site. Les 1 795
visiteurs quotidiens repartent sans laisser de trace, et rien ne permet de les
retrouver. C'est le seul actif qui appartiendrait vraiment à Constance : le
site dépend de Google, une liste d'adresses ne dépend de personne.

**13 · ~~Il n'existe aucune offre de partenariat~~ → RÉGLÉ le 26/08/2026**

Document validé par Constance et remis en PDF (2 pages, identité du site).
Trois offres : le partenariat média (échange couverture contre accès presse,
placé en premier : c'est sa vraie monnaie), l'encart de l'événement du mois
(un seul par mois, AUCUN prix publié : « conditions sur demande », grille
interne de lancement à 150 €/mois), et le Cercle en annonce. Quatre refus
écrits : présence payante dans le radar, hors-luxe, revente de billets,
affiliation dans les contenus (cohérence avec les mentions légales).
Aucun encaissement avant la structure du 21/09. Ni nom ni âge dans le
document. Clause d'indépendance reformulée en clair sur retour de Constance.


**14 · Sept établissements sans adresse utilisable**
Issu du chantier 05. Quatre ont une mauvaise boîte (Principote → boîte de
candidatures ; Nikki Beach Miami → commercial ; Eden-Roc et Hermès Ginza →
agences), trois n'en ont aucune (Dioriviera Cannes, Hôtels Barrière Deauville,
La Gritta). Cap-Ferrat a perdu la sienne : elle était nominative.

---

## ORDRE CONSEILLÉ

1. **12 — la lettre d'information.** Le seul actif qui lui appartienne.
2. **07 — la joaillerie.** Là où sont les partenaires qu'elle vise.
3. **11 — le verrou du domaine.** Cinq minutes, irréversible si négligé.
4. **13 — l'offre.** À écrire avant qu'une maison ne réponde, pas après.
5. **05 — finir les re-vérifications.** La routine s'en charge une fois le
   réseau cloud débloqué.
6. Le reste au fil de l'eau.
