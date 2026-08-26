# DOCTRINE DE LA PASSE — ConstanceParis7

> **Ce fichier fait autorité.** La routine cloud le lit à chaque exécution : il
> prime sur toute habitude générale et sur toute consigne plus ancienne.
> Pour faire évoluer la boucle, on modifie CE fichier et on pousse — aucune
> reconfiguration de la routine n'est nécessaire.
>
> Copie de référence : dépôt privé `H2SL-bot/luxe-radar-filet` (`PASSE.md`).

# PASSE.md — Doctrine complète du radar « International Luxury Events » (exécution CLOUD)

Vous mettez à jour « International Luxury Events », le radar PERPÉTUEL du luxe de la
fille de Gérald Lefebvre. Vouvoyez toujours Gérald, en français, phrases courtes.
CE SITE N'A PAS DE DATE DE FIN : la boucle tourne indéfiniment, saison après
saison (décision expresse de Gérald du 14/07/2026). Migration cloud le 21/07/2026.

## Environnement cloud (différences avec l'ancienne exécution locale)

- Cloner les DEUX dépôts en début de passe :
  - PUBLIC  : `H2SL-bot/luxe-ete-2026`   → le site (ne toucher qu'`index.html`
    + les pages générées par `tools/gen_pages.py`). `export RADAR_REPO=<chemin du clone>`.
  - PRIVÉ   : `H2SL-bot/luxe-radar-filet` → CE dépôt : le filet (`tools/`),
    la doctrine (`PASSE.md`), le journal d'apprentissage (`tools/lessons.md`),
    les journaux (`tools/run-log.ndjson`, `tools/perf-log.ndjson`, `tools/.last-count`).
- IL N'Y A PLUS de localhost:8026. Les DEUX adresses vivantes : 
  1) https://constanceparis7.com ; 2) l'artifact
  https://claude.ai/code/artifact/89b85688-ff57-481d-82d7-f7792051b066.
- MÉMOIRE DE LA BOUCLE = LE DÉPÔT PRIVÉ. Chaque passe DOIT se terminer par un
  commit+push du dépôt privé (journaux mis à jour + toute leçon nouvelle).
  Une passe qui ne pousse pas ses journaux est une passe amnésique — interdit.
- Toute erreur rencontrée → consignée dans `tools/lessons.md` ET transformée en
  contrôle permanent dans le filet (c'est la banque d'auto-amélioration exigée
  par Gérald, confirmée le 21/07/2026 : « corriger seul, améliorer seul »,
  y compris les signalements Google Search Console).

## LA MISSION (Gérald, 05/08/2026) — CE QUE LE SITE DOIT DEVENIR

**ConstanceParis7.com doit devenir LA RÉFÉRENCE MONDIALE de l'invitation aux
soirées et événements jet-set — partout dans le monde.** Pas un magazine, pas
un agenda : le radar qui SCANNE la planète et qui, pour chaque soirée
d'exception, donne la porte d'entrée et la personne à qui écrire.

Deux conséquences opérationnelles, à tenir à chaque passe :
1. COUVERTURE MONDIALE — aucune capitale du jet-set ne doit manquer. Voir la
   carte des destinations plus bas ; l'étendre dès qu'un nouveau foyer
   apparaît (nouvelle saison, nouveau resort, nouvelle scène).
2. PROFONDEUR D'ACCÈS — la valeur ne se mesure pas au nombre de fiches mais au
   nombre de PORTES OUVERTES : combien de fiches donnent un nom identifié, une
   ligne directe, un chemin réel vers le carton. C'est le seul classement où
   ce site doit être premier au monde.
Le maximum est un minimum : voir « LE CALIBRE » plus bas.

## RÈGLE DE CURATION ABSOLUE (prime sur tout)

LA RÉFÉRENCE EST L'ADN RIVIERA — Saint-Tropez, Monaco, Portofino, énergie
Festival de Cannes : glamour jet-set, tapis rouge, mondanité, gotha international.
On n'ajoute QUE l'authentiquement ultra-VIP/mondain dans des lieux d'exception
(palaces, villas/châteaux privés, galas sur invitation, clubs iconiques de la
jet-set, sport très mondain, tables étoilées événementielles fréquentées par ce
monde, semaines mode/tapis rouge). ON EXCLUT le grand public même « chic ».
Doute → ne pas ajouter. Jamais réintroduire un écarté. Pas de mention d'âge.

## PROMESSE D'ACCÈS (cœur de la valeur — directive du 15/07/2026)

Pour CHAQUE soirée mondaine/jet-set/VIP et CHAQUE défilé : viser AU MINIMUM une
voie d'accès concrète via le champ `iv` — invitation GRATUITE réaliste et/ou
place PAYANTE haut de gamme. Contact le PLUS DIRECT possible (nom + canal), MAIS
uniquement des contacts PROFESSIONNELS RÉELLEMENT PUBLIÉS (bureau de presse,
accréditation, showroom, billetterie). NE JAMAIS fabriquer un numéro/email/nom.
Sans contact vérifié : `iv.c` vide + voie officielle. Fashion Week Paris :
couvrir TOUS les défilés du calendrier FHCM + showrooms officiels (Sphère,
Tranoï, Première Classe) + programmation mode des grands magasins.

## SOIRÉES D'EXCEPTION PRIVÉES-ACCESSIBLES (directive du 17/07/2026)

Chercher en continu la soirée d'exception en cadre privé/chic où passent des
stars mondiales AVEC voie d'accès RÉELLE ET PUBLIÉE. Priorité golfe de
Saint-Tropez > Riviera italienne > reste France. Fiche retenue = soin Classement
Prestige + SÉJOUR CLÉ EN MAIN (`e.sej` {base, pitch, hotels[], tables[], exp[]},
tous RÉELS avec URL). GARDE-FOU ABSOLU : uniquement accès publié (galas à
billets/don, clubs/plages à réservation, concerts en villa vendus au public).
JAMAIS de fête privée sans billetterie, JAMAIS de contact inventé.

## BASCULE DATÉE — DIRECTION DE LA PUBLICATION AU 21/09/2026

Constance est mineure jusqu'au **21 septembre 2026**. La loi du 29 juillet 1881
impose alors que le directeur de la publication soit son représentant légal :
c'est Gerald Lefebvre qui est nommé sur `/mentions-legales.html`.

**La bascule est automatique et ne demande aucune intervention.** La règle est
écrite dans `gen_pages.py` (constante `MAJORITE`) : à la première exécution du
générateur à partir du 21/09/2026, la page est réécrite au nom de Constance
Lefebvre. Comme `gen_pages.py` est l'étape 7bis de CHAQUE passe, cela se produit
le matin même, sans que personne ait à y penser.

Si la passe du 21/09 échouait, la bascule se ferait à la première publication
suivante — jamais plus tard. Ne pas coder de date en dur ailleurs, ne pas
éditer `mentions-legales.html` à la main : le fichier est GÉNÉRÉ.

Le même jour, TROIS choses deviennent possibles et devront être proposées :

1. **Créer la micro-entreprise** — donc publier une adresse professionnelle de
   domiciliation dans les mentions légales, la loi l'exigeant dès le premier
   euro encaissé. C'est ce qui débloque l'offre payante (« Le dossier », 500 €,
   annoncée pour septembre).
2. **Remettre son âge sur `/a-propos.html`** si elle le souhaite — retiré
   volontairement le 20/08/2026 tant qu'il révélait sa minorité.
3. **Ouvrir la lettre d'information** (chantier 12), décidée le 21/08/2026 et
   volontairement reportée à la majorité : collecter des adresses fait de
   Constance une responsable de traitement au sens du RGPD, ce qui relève de
   son représentant légal tant qu'elle est mineure. Tout se prépare avant, les
   inscriptions n'ouvrent qu'à cette date.
   **Forme retenue : hebdomadaire, le vendredi matin, centrée sur LES DÉLAIS**
   — « il vous reste 6 jours pour demander votre accréditation à X », les
   portes qui s'ouvrent et celles qui se ferment. Pas un digest d'événements :
   le site le fait déjà, et personne ne s'abonne à ce qu'il peut consulter.
   L'actif réel, ce sont les échéances des 306 voies d'entrée, que personne
   d'autre ne suit.
   Conditions RGPD : case à cocher vide, double confirmation, finalité
   annoncée, désabonnement en un clic, page de confidentialité. Outil
   pressenti : Brevo (société française, serveurs UE, gratuit à ce volume).
   **AVERTISSEMENT** : l'ajout d'un formulaire cassera probablement la pureté
   actuelle du site (0 cookie, 3 requêtes) et rendra FAUSSE la phrase « Aucun
   cookie n'est déposé » des mentions légales. Les mettre à jour le même jour,
   sans quoi le site mentira là où il promet la rigueur.

## PROTECTION DES PERSONNES — AUCUNE COORDONNÉE NOMINATIVE EN PUBLIC (directive de Constance, 20/08/2026)

Le site publiait l'adresse e-mail et la ligne directe de 610 personnes physiques
— pour l'essentiel des attachés de presse. Devant 1 800 visiteurs par jour, cela
transformait le radar en annuaire de démarchage, aux dépens exacts des gens dont
il faut devenir le partenaire. Retiré le 20/08/2026 : 626 coordonnées sur
124 fiches.

**CE QUI EST INTERDIT EN PUBLIC**
- l'adresse e-mail nominative d'une personne (`prenom.nom@`, `p.nom@`, `prenom@`) ;
- son portable, et toute ligne présentée comme « directe » ou « mobile ».

**CE QUI RESTE, ET QUI DOIT RESTER**
- le **nom et la fonction** : information éditoriale légitime, publiée par les
  sources officielles, et utile au lecteur pour comprendre la voie ;
- **toutes les voies de service** : `press@`, `info@`, `rsvp@`, `reservations@`,
  `billetterie@`… y compris chez un petit organisateur qui utilise Gmail —
  `presse.festivalramatuelle@gmail.com` est une boîte de service, pas une personne ;
- les **standards**, **billetteries**, **formulaires** et **URL officielles**.

**GARDE-FOU — LA LOI DU SITE PRIME**
Une fiche ne perd JAMAIS sa dernière porte d'entrée. Si le retrait devait la
laisser sans aucune voie, la fiche est laissée intacte et signalée. Le nettoyage
cède devant la promesse d'accès, jamais l'inverse.

**OÙ VONT LES COORDONNÉES RETIRÉES**
Dans le coffre Obsidian : `Référence/Carnet de contacts presse.md`. Elles ne
sont pas détruites — elles valent bien plus en privé qu'en public. C'est le
carnet d'adresses à utiliser pour les partenariats, une personne à la fois.

**OUTILS**
`.radar/tools/contacts_classer.py` — décide si une adresse est une voie de
service ou la coordonnée d'une personne, par croisement avec les noms que le
site a lui-même enregistrés (jamais par devinette).
`.radar/tools/contacts_nettoyer.py --blanc` — essai, n'écrit rien.
`.radar/tools/contacts_nettoyer.py --appliquer` — applique, français ET les
12 traductions (le verdict rendu sur le français s'impose aux 12 langues).

**À CHAQUE PASSE** : toute fiche créée ou enrichie passe par cette règle avant
publication. Une coordonnée nominative qui réapparaît est un défaut, pas un
enrichissement.

## LA LOI DU SITE — UN ÉVÉNEMENT = UNE INVITATION + UN SÉJOUR (directive fondatrice, 28/07/2026)

La raison d'être de ConstanceParis7 : que Constance soit INVITÉE aux événements
qu'elle liste. Chaque fiche doit donc ouvrir DEUX portes, quelle que soit la
localisation :
1. LA PORTE DE L'INVITATION (`iv`) : la voie la plus DIRECTE vers le carton —
   bureau de presse, agence RP de l'événement, responsable invitations,
   billetterie haut de gamme. Cible : 100 % des fiches mondaines. Toujours des
   contacts PROFESSIONNELS PUBLIÉS ; ne JAMAIS inventer (c'est la crédibilité
   de Constance qui se joue).
2. LA PORTE DU SÉJOUR (`e.sej`) : palace(s) à côté, table(s) étoilée(s) ou
   iconique(s), expérience(s) — tous RÉELS avec URL. UN ÉVÉNEMENT = UN SÉJOUR,
   sans exception de lieu ni de taille.
Toute NOUVELLE fiche naît COMPLÈTE (iv + sej + traductions). RATTRAPAGE de
l'existant par vagues quotidiennes : fenêtre live (auj.→+90j) d'abord, les
plus imminents et les mieux notés en tête, ~10-15 séjours par passe, recherche
réelle + vérification adversariale, puis traduction aux passes suivantes.
Exceptions de bon sens : les fiches-conseil et dossiers d'accès (c=acces)
n'ont pas de séjour propre.

## LES PAGES GOOGLE DISENT CE QUI FAIT LA VALEUR (leçon du 29/07/2026)

Signalement Search Console « Explorée, actuellement non indexée » : les pages
indexables existaient mais TAISAIENT le cœur de valeur — le séjour clé en main
n'y était pas, et sur les pages FRANÇAISES la voie d'invitation non plus (bug :
`T()` cherchait un champ plat `iv_o` alors que le français vit dans
`e["iv"]["o"]`). Des pages de 154 mots : Google les explorait sans les indexer.
Corrigé le 29/07 (fiche type 154 → 487 mots). RÈGLE : tout ce qui fait la valeur
d'une fiche (accès + séjour) DOIT arriver sur la page que Google lit, dans les
13 langues. `validate.py` le vérifie désormais sur pièces à chaque passe et
BLOQUE si une page indexable tait son séjour ou sa voie d'invitation (il
signale aussi les pages sous 120 mots). Ne jamais neutraliser ce contrôle :
c'est lui qui a rendu le site indexable.

## LE CALIBRE — LE MAXIMUM EST UN MINIMUM (directive de Gérald, 05/08/2026)

**INVITATIONS — viser LA PERSONNE, pas le service.** Un « bureau de presse »
ou un `contact@` est un REPLI, pas la cible. Chercher et nommer :
- le NOM ET PRÉNOM de l'attaché(e) de presse, du directeur/de la directrice de
  la communication, du responsable des partenariats, du chargé des invitations,
  du concierge chef, du directeur du club — avec sa FONCTION EXACTE ;
- **SON PORTABLE — c'est LA priorité absolue.** Un standard (+33 1…, +41 33…)
  ne sert à rien : il filtre. Le mobile de l'attaché(e) de presse est la porte
  qui s'ouvre vraiment. Ces numéros SONT publiés, massivement : les communiqués
  et dossiers de presse affichent presque toujours « Contact presse : Prénom
  Nom — 06 XX XX XX XX ». C'est le gisement à exploiter en priorité.
- son e-mail nominatif (prenom.nom@…) plutôt qu'une boîte générique ;
- OÙ CHERCHER, par ordre de rendement : (1) les COMMUNIQUÉS DE PRESSE et
  dossiers de presse en PDF — c'est là que vivent les portables, en bas de
  page, sous « Contact presse » ; (2) les pages « Espace presse » / « Media »
  des lieux et organisateurs ; (3) l'ours du programme officiel ; (4) les
  agences RP mandatées (leurs communiqués nomment l'attaché en charge du
  dossier, avec son mobile) ; (5) mentions légales, avis de course, rapports
  annuels de fondation ; (6) page « équipe » du lieu.
  RÉFLEXE : chercher explicitement « contact presse » + le nom de l'événement,
  et ouvrir les PDF — les portables y sont, rarement dans le HTML.
Une fiche avec un nom identifié vaut dix fiches avec une adresse générique :
c'est ce qui transforme une demande anonyme en conversation.
GARDE-FOU INCHANGÉ ET ABSOLU : ce nom doit être RÉELLEMENT PUBLIÉ et vérifié
pendant la recherche. Jamais un nom deviné, jamais une fonction supposée,
jamais un e-mail reconstruit par déduction (prenom.nom@…). Sans nom vérifié :
le contact générique, et on le dit franchement.

**LA VOIE GRATUITE — la chercher systématiquement et la QUALIFIER.** Le champ
`iv.g` ne doit jamais être bâclé. Pour chaque événement, chercher explicitement
laquelle de ces cinq portes existe, et le dire précisément :
1. ACCRÉDITATION PRESSE — la porte principale et gratuite. Nommer le formulaire,
   la date limite, les pièces demandées, la personne qui l'instruit. Préciser
   qu'elle est nominative et non transmissible quand c'est le cas.
2. PARTENARIAT MÉDIA — le seul cadre légitime pour qu'un site FASSE GAGNER une
   invitation : l'organisateur accorde un quota et valide l'opération. À
   signaler quand l'événement en pratique (jeux-concours co-organisés).
3. INVITATION PAR UN MEMBRE / PARRAINAGE — clubs fermés, cercles.
4. MÉCÉNAT ET CONTREPARTIES — galas caritatifs : sièges offerts par les mécènes.
5. TIRAGE AU SORT / BILLETTERIE PUBLIQUE — rare mais réel.
Si AUCUNE porte gratuite n'existe, l'écrire franchement : « aucune voie gratuite
publiée ». Ne jamais laisser croire qu'une invitation s'obtient quand elle
s'achète. Et ne JAMAIS suggérer de revendre ou céder une accréditation
nominative : c'est ce qui grille une relation presse pour toujours.

**CADENCE DE TRAVAIL — ne jamais affamer les vérificateurs.** La concurrence
est plafonnée (16 agents) : un gros lot recherche→vérification occupe toutes
les places avec des chercheurs et AUCUN vérificateur ne démarre — donc rien
n'est publiable. Travailler par lots de 8-10, ou séparer en deux chantiers
(un qui cherche, un qui vérifie ce qui est déjà cherché). PUBLIER AU FIL DE
L'EAU à chaque lot vérifié : une limite de session ne doit jamais faire
perdre du travail abouti.

**SÉJOURS — calibre jet-set, sans exception.** Palaces et 5 étoiles réels,
tables étoilées ou institutions iconiques, expériences d'exception
(hélicoptère, yacht privatisé, visite privée hors horaires, spa signature).
Jamais de « bon hôtel » ni de « bonne table » : le standard est celui du
Cheval Blanc, du Louis XV, des Caves du Roy. Si la ville n'offre rien de ce
calibre, en mettre moins plutôt qu'en mettre de moindre.

## LE PRINTEMPS 2027 EST VIDE (constat du 22/08/2026)

Comptage du 22/08 sur les fiches à venir : **mars 4 · AVRIL 0 · mai 4 · juin 1**.
Un visiteur qui prépare un voyage au printemps prochain ne trouve rien. Et c'est
MAINTENANT que les grandes maisons publient leurs dates : attendre janvier, c'est
arriver après tout le monde, quand les accréditations sont closes et les hôtels
pleins.

**HUIT ANCRES VÉRIFIÉES LE 22/08/2026**, à créer en priorité — nées COMPLÈTES
(voie d'entrée + séjour + 13 langues) :

| Événement | Dates | Lieu |
|---|---|---|
| TEFAF Maastricht | **13-18 mars 2027** | MECC Maastricht |
| Art Basel Hong Kong | **25-27 mars 2027** | HKCEC |
| Watches and Wonders | **5-11 avril 2027** | Palexpo, Genève |
| Salone del Mobile (65e) | **13-18 avril 2027** | Rho Fiera, Milan |
| Festival de Cannes (80e) | **11-22 mai 2027** | Palais des Festivals |
| GemGenève | **11-14 mai 2027** | Palexpo, Genève |
| Grand Prix de Monaco | **3-6 juin 2027** | Circuit de Monaco |
| Royal Ascot | **15-19 juin 2027** | Ascot, Berkshire |

**À RECONFIRMER À LA SOURCE avant publication** : le Grand Prix de Monaco est
donné « sous réserve d'approbation par le Conseil Mondial du Sport Automobile de
la FIA ». Ne pas le publier sans l'avoir revérifié sur acm.mc. Les sept autres
proviennent des organisateurs eux-mêmes ou de leur presse spécialisée.

**LE FUORISALONE** (Milano Design Week, 12-18 avril 2027) accompagne le Salone :
c'est une seconde fiche légitime, pas un doublon — l'un est un salon payant à
Rho, l'autre un parcours gratuit dans la ville.

**DEUX CHANTIERS, UN SEUL EFFORT.** Watches and Wonders et GemGenève comblent à
la fois ce trou et celui de la joaillerie. Les créer une fois sert les deux
consignes ; ne pas les compter deux fois.

**ENSUITE, ÉLARGIR.** Ces huit ancres ne sont qu'un socle. Le printemps porte
aussi : Paris et Milan Fashion Week (automne-hiver 27-28), le Bal de la Rose à
Monaco, les ventes de printemps de Christie's et Sotheby's, Chelsea Flower Show,
les 24 Heures du Mans, la saison d'opéra de Vienne et de Milan, Art Basel Bâle
en juin. Une par passe, comme le reste.

## LES GUIDES D'ACCÈS — LE CONTENU QUI TRAVAILLE TOUT SEUL (21/08/2026)

Le radar tient **10 fiches `c=acces`** pour 295 fiches d'événements. Or une fiche
d'événement meurt le lendemain de l'événement, tandis qu'un guide reste vrai des
années, se traduit une fois, et répond à ce que les gens tapent réellement dans
Google : « comment se faire inviter à… », « accréditation presse … ». Gérald
l'avait déjà inscrit au RESTE-À-FAIRE le 29/07 ; c'est toujours le levier de
visibilité le plus rentable et le moins entamé.

**UN GUIDE N'EST PAS UNE FICHE PAR ÉVÉNEMENT.** Il décrit UNE PORTE, et sert
d'un coup toutes les fiches qui l'empruntent. Il en faut une trentaine au total,
pas trois cents.

**LES SIX À ÉCRIRE, dans cet ordre.** Comptage fait le 22/08/2026 sur les 295
fiches de la fenêtre live — le chiffre est le nombre de fiches que chaque guide
desservirait :

| Guide | Fiches desservies |
|---|---|
| 1. Obtenir une accréditation presse | **145** |
| 2. Passer par une agence de relations presse | 67 |
| 3. Se faire inscrire sur une liste d'invités (RSVP) | 51 |
| 4. Réserver une table là où c'est réputé impossible | 33 |
| 5. Entrer à un vernissage ou une preview privée | 28 |
| 6. Comprendre les tirages au sort et les ballots | 7 |

**ÉCARTÉ SCIEMMENT : « acheter un billet en ligne »**, malgré 158 fiches. Il n'y
a aucune méthode à révéler, donc aucune recherche à capter. Le volume ne fait
pas la valeur.

**FAIT LE 24/08/2026 : les six guides existent.** Le n° 1 (accréditation) le 21/08 par la passe ; les n° 2 à 6 le 24/08, chacun rédigé depuis le corpus des fiches qui décrivent sa porte (aucun exemple inventé, vérification mécanique), contre-lu, publié en 13 langues. La consigne de passe devient : ENTRETENIR — quand une passe corrige une fiche citée en exemple dans un guide, vérifier que l'exemple reste vrai ; et signaler toute porte nouvelle qui mériterait un 7e guide.

**Matière déjà disponible pour le guide n° 1**, sans rien inventer : les 145
fiches concernées décrivent chacune une procédure d'accréditation réelle et
vérifiée. Le guide se construit en dégageant ce qu'elles ont en commun —
l'anticipation de trois semaines, l'organe de rattachement demandé, les portails
d'inscription, le fait qu'une boîte « info@ » soit souvent un répondeur qui
renvoie au téléphone (constaté le 21/08 chez La Rose des Vents). Citer des
exemples nommés tirés des fiches, jamais un cas fabriqué.

**PLACE DANS L'ORDRE DES PRIORITÉS.** Après le piège du « 31 août », qui a une
échéance ferme. Avant la joaillerie, qui n'en a pas.

## LE BANDEAU « OUVERTURES & DÉLAIS » (posé le 26/08/2026)

L'accueil porte, sous le masthead, un bandeau `section.portes` : les fenêtres
de réservation qui ouvrent ou ferment (ex. « Boucheron : réservations le
2 sept, 10 h »). C'est la signature du site rendue visible : arriver avant
les autres. C'est aussi l'antichambre de la lettre d'information du 21/09,
qui dira la même chose par courriel.

RÈGLE DE PASSE : à chaque passe, (a) AJOUTER toute nouvelle fenêtre datée
découverte dans les fiches (ouverture de billetterie, d'inscriptions, de
candidatures) ; (b) RETIRER les entrées périmées : chaque entrée porte un
`data-exp="AAAA-MM-JJ"` et validate.py signale celles dont la date est
passée. 3 à 6 entrées maximum : c'est une vitrine, pas une liste. Entrées
en français compact, chiffres universels, lien vers la fiche. Le titre du
bandeau est traduit (clé i18n `portes_t`).

LE BADGE « VÉRIFIÉ À LA SOURCE » : les pages événement affichent la date de
vérification quand elle est ÉCRITE dans `so` ou `iv` (motif « vérifié le
JJ/MM/AAAA ») — 128 pages au 26/08. Pas de date écrite, pas de badge : on
n'affiche jamais une rigueur qu'on ne peut pas prouver. En consigner une à
chaque vraie vérification augmente la couverture naturellement.

## LES TEXTES SAISONNIERS DE L'INTERFACE (règle du 24/08/2026)

La relecture native des 12 langues a trouvé l'accueil encore en « juillet et
août » un 24 août : les textes éditoriaux de saison n'avaient aucun mécanisme
de rafraîchissement. Le badge `brandline_season` bascule tout seul aux
équinoxes (`saison.py`), mais personne ne bascule la prose.

RÈGLE : trois clés du dictionnaire d'interface sont SAISONNIÈRES et datées :
`brandsub`, `intl_p1`, `intl_p2` (le sous-titre et les deux paragraphes du
circuit mondial). **À chaque équinoxe et solstice, quand `saison.py` change le
badge, réécrire ces trois clés en français depuis les fiches de la saison,
puis les retraduire dans les 12 langues.** Jamais l'inverse, jamais partiel :
un français neuf avec des traductions anciennes est une divergence muette.

Toutes les autres clés ont été rendues NEUTRES le 24/08/2026 (« cette
saison », « la saison en cours ») précisément pour ne plus jamais périmer :
ne pas y réintroduire de mois ni de saison nommée.

## LA JOAILLERIE EST LE TROU DU RADAR (constat du 20/08/2026)

Le site annonce à Google, dans sa propre description : « défilés, **haute
joaillerie**, polo, galas, ventes aux enchères ». Il tient **2 fiches** de
joaillerie en fenêtre live, contre 92 festivals. C'est le seul endroit du site
qui promet ce qu'il ne livre pas.

Les deux fiches existantes sont des expositions de musée à Paris (Van Cleef &
Arpels, Daniel Brush). **Aucun lancement de collection, aucune vente, aucun
salon.** Une troisième fiche gonflait le compteur par erreur : The I.C.E. St.
Moritz, qui est un concours d'élégance automobile — reclassée en `artdevivre`
le 20/08/2026, comme Chantilly et Pebble Beach.

**POURQUOI C'EST LA PRIORITÉ.** Ce sont les maisons joaillières qui ont un
service de presse, un budget et des soirées sur invitation. Un festival n'a
rien de tout cela. La catégorie la plus faible du radar est exactement celle où
se trouvent les partenaires visés.

**LE CALENDRIER TOMBE DANS LES MOIS VIDES** — un seul effort comble deux trous
(voir aussi le reste-à-faire : automne et printemps 2027) :

| Événement | Dates vérifiées le 20/08/2026 | Mois aujourd'hui |
|---|---|---|
| Sotheby's Fine Jewelry, Genève | 30/10 → 13/11/2026 (expo 6-10/11) | nov. : 18 |
| **Watches and Wonders**, Genève | **5 → 11 avril 2027** (public 9-11) | **avril : 0** |
| GemGenève, Palexpo | 11 → 14 mai 2027 | mai : 4 |

**ORDRE DE PRIORITÉ, fixé le 21/08/2026 au soir.** Le réseau sortant a été
ouvert (« Accès réseau : Complet ») : la passe du 22/08 est la première à
pouvoir vérifier dehors. Deux chantiers l'attendent, et ils ne sont pas
également pressés :

1. **D'ABORD le piège du « 31 août »** — 14 fiches restantes au 22/08 (21 ont
   été établies par la passe du matin). Ce sont des établissements réels dont
   la fin de saison est un bouchon. Elles DISPARAÎTRONT de l'écran
   le 1er septembre, la plupart à tort. Échéance ferme, contenu vrai à sauver.
   Établir ces dates à leur source officielle passe avant tout le reste.
2. **PUIS les guides d'accès** — six à écrire, voir la section dédiée. C'est
   le levier de visibilité le plus rentable et le moins entamé.
3. **ENSUITE la joaillerie** — 8 fiches à créer. Aucune échéance.

Perdre du contenu exact coûte plus cher que de ne pas encore en avoir ajouté.
Une fois les 22 dates établies, revenir à la règle ci-dessous.

**À CHAQUE PASSE, tant que la joaillerie est sous 10 fiches en fenêtre live :
créer une fiche joaillière née COMPLÈTE** (voie d'entrée + séjour + 13 langues),
avant tout autre ajout. Pistes : Watches and Wonders, GemGenève, Vicenzaoro,
ventes Christie's et Sotheby's de Genève, Biennale Paris, PAD, TEFAF, Doha
Jewellery & Watches, et les lancements de haute joaillerie de juillet à Paris
pendant la semaine de la couture.

**Ne pas gonfler le compteur.** Une exposition qui cite une maison n'est pas une
fiche de joaillerie ; un concours automobile sponsorisé par un horloger non
plus. La catégorie `joaillerie` est réservée aux événements dont la joaillerie
ou la haute horlogerie est le SUJET.

## LE PIÈGE DU « 31 AOÛT » (constat du 20/08/2026)

**46 fiches de la fenêtre live se terminent exactement le 31/08/2026** — 14 % du
site. Ce n'est pas une date : c'est un bouchon posé quand la vraie fin de saison
n'était pas connue. Le voile d'affichage les ferait toutes disparaître le
1er septembre, la plupart à tort.

Quatre ont été vérifiées le 20/08/2026 à leur source officielle. **Les quatre
étaient fausses**, toutes dans le même sens — l'événement dure plus longtemps :

| Fiche | Portée | Réel |
|---|---|---|
| David Guetta / Ushuaïa | 31/08 | 05/10 (résidence du lundi) |
| Nikki Beach Mallorca | 31/08 | 11/10 |
| LIV at Fontainebleau | 31/08 | 27/09 au moins |
| Ritual Club Baja Sardinia | 31/08 | 13/09 |

**RÈGLE.** Une date de fin au 31/08 (ou au 31/12, 18 fiches) doit être traitée
comme NON RENSEIGNÉE tant qu'une source officielle ne la confirme pas. Priorité
haute avant le 1er septembre : les 42 restantes sont à reprendre une par une.
Ne jamais poser une fin de saison « par défaut » : mieux vaut inscrire le doute
au registre que tronquer un événement réel.

## VOILE D'AFFICHAGE (directive du 28/07/2026)

L'internaute ne voit JAMAIS un événement terminé : un voile côté écran retire
de toutes les rubriques toute fiche dont la date de fin est passée (dossiers
d'accès exceptés), et l'agenda démarre au jour même. Rien n'est supprimé :
les données gardent les terminés 30 jours (purge du plancher). Ne pas
« réparer » une fiche absente de l'écran mais présente dans les données :
c'est le voile qui fait son travail.

## LE RESTE-À-FAIRE, DANS L'ORDRE (état du 29/07/2026 — à tenir à jour)

Le site publie 537 événements. Il n'est PAS complet : la LOI DU SITE n'est
honorée qu'à moitié. Priorité de chaque passe, dans cet ordre strict :

PLAN VALIDÉ PAR GÉRALD le 29/07/2026 — ordre STRICT :
1. **TRADUIRE les fiches nues** — 62 fiches EN LIGNE mais lisibles en français
   seulement (tour du monde + renfort du 29/07 ; 3 déjà faites). Le plus
   urgent : un visiteur non francophone tombe sur une fiche illisible.
   ~10-15 fiches par passe, toutes langues manquantes, une fiche par agent
   (les lots de 3 fiches échouent : trop lourd, l'agent s'arrête à la 1re).
2. **COMBLER L'AUTOMNE** — le radar s'effondre après septembre (oct. : 20
   fiches, nov. : 16). Ajouter 40-60 événements d'exception oct.-nov.-déc. :
   grands bals, galas de rentrée, ventes aux enchères du soir, saisons d'opéra,
   Art Basel Paris et son orbite. Nés COMPLETS (invitation + séjour + langues).
3. **ÉCRIRE 10 NOUVEAUX GUIDES D'ACCÈS** (c=acces) — il n'y en a que 11 alors
   que c'est le contenu le plus cherché sur Google (« comment être invité
   à… »). Guides par lieu ou par circuit : Caves du Roy, paddock F1, bals de
   Vienne, ventes Christie's/Sotheby's, front row Fashion Week, etc.
   Intemporels, traduits une fois, carburant du référencement.
4. **PUIS séjours restants** (372, dont 227 fenêtre live, prestige d'abord)
   **et voies d'invitation** (243 manquantes, cible 100 %).
À chaque passe : recompter traductions/séjours/invitations manquants et
donner les 3 chiffres au compte rendu. Jamais « à jour » tant que non nuls.

À chaque passe, RECOMPTER ces quatre chiffres et les donner dans le compte
rendu : c'est le seul tableau de bord honnête. Ne jamais annoncer le site
« à jour » tant qu'ils ne sont pas à zéro.

## HORIZON ROULANT

- Couvrir en permanence AUJOURD'HUI → +90 JOURS.
- Suivre les SAISONS du circuit (été Riviera ; sept-oct Fashion Weeks, Voiles,
  Monaco Yacht Show, Art Basel Paris, Mostra ; hiver Courchevel/Gstaad/St-Barth/
  Miami ; printemps Cannes, GP Monaco, Met Gala…). Toujours sous filtre Riviera.
- PURGE à chaque passe complète : supprimer les événements d2 < aujourd'hui-30j
  (baisse de compte normale — l'indiquer au compte rendu).
- CARTE DES DESTINATIONS À CONQUÉRIR (Gérald, 28/07/2026 — « toutes les
  soirées d'exception du monde entier ») : intégrer PROGRESSIVEMENT, ~1
  destination nouvelle par passe quand la fenêtre live est saine, toujours
  sous filtre Riviera et LOI DU SITE (invitation + séjour dès la naissance) :
  Lac de Côme (Villa d'Este), Taormine, Comporta/Melides, Sotogrande (polo),
  Riviera d'Athènes/Spetses/Porto Heli, Hvar/Dubrovnik, Vienne (saison des
  bals, Opernball), Megève/Kitzbühel, Los Angeles (LACMA Art+Film, Vanity
  Fair Oscars, amfAR LA), Aspen, Rio (réveillon Copacabana Palace, Carnaval
  VIP), Punta del Este, Buenos Aires (polo Palermo), Tulum/Careyes,
  Riyad/AlUla, Singapour (GP de nuit), Hong Kong (Art Basel HK), Bali,
  Mumbai/Udaipur (galas NMACC, grands mariages), Maldives (réveillons),
  Mustique (Basil's Bar NYE), Harbour Island, Casa de Campo, F1 mondaine
  (Las Vegas, Miami), Melbourne Cup (Birdcage).
- BRANDING : « ConstanceParis7 » (logotype capitales, 7 en or — NE JAMAIS
  TOUCHER). Ligne d'édition « International Luxury Events · Été 2026 ». Vers le 25 août,
  proposer à Gérald le rafraîchissement « Automne 2026 » — sans renommer seul.

## OÙ VIT LA VÉRITÉ — À LIRE AVANT TOUTE ÉDITION (bascule du 22/07/2026)

Depuis la bascule perf, le dépôt contient **trois artefacts** et il ne faut jamais
les confondre :

| Fichier | Rôle | Qui l'écrit |
|---|---|---|
| **`index-full.html`** | **SOURCE DE VÉRITÉ de travail — PLUS VERSIONNÉ** (il faisait grossir le dépôt de 10,7 Mo/jour et alourdissait chaque clonage). **Absent d'un clone frais : le reconstruire AVANT tout avec `python3 .radar/tools/rebuild_full.py`** (somme exacte de index.html + i18n-data/, vérifiée fidèle au fichier près). C'est LUI qu'on lit et modifie ensuite. | vous, à chaque passe |
| `index.html` | Ce que voit l'internaute : français seul + chargeur. ~9x plus léger (0,40 Mo gzip contre 3,82). **GÉNÉRÉ — ne jamais l'éditer à la main.** | `split_i18n.py` |
| `i18n-data/<lang>.json` | Une langue par fichier, chargée à la demande, indexée par clé stable « d1\|nom ». **GÉNÉRÉ.** | `split_i18n.py` |

**Conséquence pratique : d'abord `python3 .radar/tools/rebuild_full.py` (recrée index-full.html), puis lire et écrire `index-full.html`, puis lancer
`python3 .radar/tools/split_i18n.py --apply` qui régénère `index.html` et
`i18n-data/`. Publier les trois.** Éditer `index.html` directement ferait perdre
les traductions au prochain passage de l'outil.

Si le chargement d'une langue échoue chez l'internaute, l'affichage retombe sur
le français : jamais de page vide, jamais de contenu perdu.

### Champs d'une fiche (dans `index-full.html`)

n, z (paris|sainttropez|cotedazur|province|international), g, c (mode|joaillerie|
art|sport|festival|artdevivre|autre|acces), v, l, dt, d1/d2 (ISO), h, ht, a, p, u,
ds, pe, ci, so, cf, ct, sv/sp/sl (0-100), sw (130 car. max), iv ({o,g,c:[{t,v}],w}),
dc (valeur EXACTE de la liste des codes vestimentaires — recopier telle quelle,
accents compris, depuis une fiche existante), tr = traductions
{en|es|it|pt|de|ru|ar|zh|ja|ko|hi|tr : {n, dt, ds, sw, p, pe, ci, ht, iv_o, iv_g,
iv_w, sej_*}} (piège de nommage : `e.tr.tr` = le TURC — le champ et le code de
langue portent le même nom, c'est normal). PRÉSERVER `tr` à la réinjection.
Échapper « </ » en « <\/ ». Le head SEO, le bloc ld+json et le bloc i18n
(interface 13 langues) ne se touchent pas.

## CADENCE — UNE PASSE PAR JOUR (5h55 Paris — demande de Gérald du 28/07/2026)

Décision de Gérald du 22/07/2026 : **la passe du soir est supprimée.** Elle
vérifiait les événements à +2 jours, ce que la passe du matin fait déjà sur
7 jours (étape 2b) : elle était redondante, sauf pour un changement survenu
entre 7h et 19h — valeur trop mince pour un radar à horizon +90 jours. Deux
raisons de plus : chaque passe réécrit le bloc `data` (c'est ce qui a effacé
15 fiches le 21/07), et une seule passe tient mieux dans le quota.

Il n'y a donc plus qu'un mode : la PASSE COMPLÈTE du matin (procédure
ci-dessous). Si une passe du soir devait être rétablie un jour, sa seule
justification serait la veille d'annonces intra-journée en pleine saison —
à rediscuter avec Gérald, jamais à réactiver d'office.

Le filet de surveillance tolère 2 jours sans mise à jour : avec une passe
quotidienne, une matinée ratée reste sous le seuil et se rattrape le
lendemain. Le seuil n'est donc pas à changer.

## LAISSER UNE TRACE DANS LE DÉPÔT — AVANT ET APRÈS (22/07/2026)

Gérald ne doit RIEN avoir à faire, jamais — pas même ouvrir un e-mail. Le
système doit donc se diagnostiquer seul. Pour cela, laissez deux traces dans le
dépôt, et poussez-les.

**1. DÈS LE DÉBUT, avant tout travail** (c'est le plus important : si vous
mourez en route, cette trace prouvera au moins que vous aviez démarré) :

```
mkdir -p .radar/journal
date -u +'%Y-%m-%dT%H:%M:%SZ  DEMARRAGE' >> .radar/journal/passages.log
git config user.name  "radar-routine-claude"
git config user.email "radar-routine@users.noreply.github.com"
git add .radar/journal/passages.log
git commit -m "Passage : démarrage"
git push origin HEAD:main || git push origin HEAD:claude/passage-$(date -u +%Y%m%d-%H%M)
```

Si même ce push échoue, ce n'est pas grave : continuez la passe. Mais notez-le
dans votre compte rendu, c'est un signal capital.

**2. À LA FIN**, écrivez votre compte rendu complet dans
`.radar/journal/dernier-compte-rendu.md` (écrasez le précédent) et ajoutez une
ligne `... FIN — <résumé en une phrase>` à `passages.log`. Poussez le tout.

Ce journal est lu par les contrôles automatiques et par toute session future.
C'est ce qui permet de savoir ce qui s'est passé sans déranger Gérald.

## SIGNATURE OBLIGATOIRE DES COMMITS (22/07/2026)

**AVANT tout commit, posez votre identité git :**

```
git config user.name  "radar-routine-claude"
git config user.email "radar-routine@users.noreply.github.com"
```

Ce n'est pas cosmétique. Un bulletin quotidien automatique
(`.github/workflows/bulletin-quotidien.yml`) dit chaque matin à Gérald si la
routine a travaillé, et il le détermine **par la signature des commits**. Le
plancher signe `radar-passe-quotidienne`, vous signez `radar-routine-claude`,
tout le reste est considéré comme du travail manuel et n'est pas compté.

Si vous ne signez pas, votre travail passera pour manuel et Gérald recevra une
alerte « la routine n'a rien publié » alors que vous aurez tourné.

## PUBLICATION — FILET AUTOMATIQUE (22/07/2026)

Poussez sur `main`. **Si le push sur `main` est refusé, poussez sur une branche
`claude/<quelque-chose>` : un workflow GitHub la reverse automatiquement dans
`main` dans la minute** (`.github/workflows/publier-branche-claude.yml`). Le site
se met donc à jour dans les deux cas — la publication ne dépend plus du réglage
« Allow unrestricted branch pushes ».

Signalez tout de même le repli dans votre compte rendu, pour qu'on sache que le
réglage manque. En cas de conflit de fusion, le workflow n'écrase rien et ouvre
une issue GitHub.

## PROCÉDURE — LA PASSE (matin, 5h55)

0. Cloner les 2 dépôts, `export RADAR_REPO=<clone public>`, puis
   `bash tools/precheck.sh` (verrou, cadence, run interrompu, validate).
1. Extraire le JSON id="data" d'**index-full.html** (la source complète). Ne jamais casser head ni i18n.
2. Recherche web (agents parallèles, échelle modérée), fenêtre auj.→+90j,
   filtre Riviera : a) nouveaux événements jet-set (France/Riviera puis circuit
   international de saison) ; b) vérifier les événements des 7 prochains jours +
   tester leurs liens u.
3. Fusionner (sans doublon nom+ville), scores (gala mondain ≈ 85+, VIP/palace
   ≈ 60-84), sw, iv, dc. PURGER d2 < auj.-30j.
4. TRADUIRE les nouveaux en 12 langues (en, es, it, pt, de, ru, ar, zh, ja, ko, hi, tr) —
   agents parallèles. Ne pas traduire noms propres/marques ; dt = mots traduits,
   chiffres gardés ; emails/URLs/prix inchangés ; JAMAIS « &amp; » (& reste &).
   QUALITÉ RUSSE : pas d'article français résiduel ; villes en cyrillique ;
   « 20:00 » jamais « 20h » ; édition → « выпуск »/ordinal ; palace →
   « палас-отель » ; takeover en latin ; sensoriel → « сенсорный ».
   ALLEMAND : Sie ; exonymes (Mailand, Venedig, Neapel). ARABE (fusha) : villes
   translittérées (باريس, نيويورك, ميلانو — marques en latin) ; « 10:30 » ;
   calendrier → « تقويم » ; couture → « الأزياء الراقية ».
   HINDI : devanagari, registre luxe (pas de hinglish hors फ़ैशन/गाला/पोलो) ;
   villes translittérées (पेरिस, मोनाको, सेंट-ट्रोपे) ; marques en latin ;
   « 20:00 » ; chiffres occidentaux. TURC : orthographe TDK (İ/ı, ş, ğ, ç, ö, ü) ;
   exonymes (Monako, Venedik, Milano, Londra) ; Paris/Saint-Tropez/Cannes
   inchangés ; dates à la turque (« 9 Ağustos 2026 »).
   RÈGLE DE COHÉRENCE : corriger un champ FRANÇAIS rend sa traduction fausse —
   retirer alors cette clé dans chaque langue (l'affichage retombe sur le
   français, exact) plutôt que de laisser un horaire faux traduit en 12 langues.
   RÈGLE DE FUSION : apparier les traductions par le NOM de la fiche, jamais par
   sa position dans le tableau (une passe concurrente peut avoir inséré des
   événements entre-temps).
4ter. BACKFILL `sej` — RÈGLE PERMANENTE depuis la LOI DU SITE : chaque passe,
   (a) composer ~10-15 séjours pour les fiches de la fenêtre live qui n'en ont
   pas (prestige d'abord ; recherche web réelle + vérification adversariale —
   la vague 1 du 28/07 au soir a porté le compte à 112/470) ; (b) traduire par
   lots les séjours sans sej_pitch dans certaines langues (les 16 de la vague 1
   sont à traduire). Jamais traduire noms propres ni URLs.
   RÉVISION HINDI — TERMINÉE le 28/07/2026 au soir : 8/8 lots relus
   (470 fiches), 144 corrections appliquées après contre-vérification
   adversariale, harmonisation faite (« मिशेलिन स्टार » unique, तरणताल).
   Il ne reste que l'entretien : toute NOUVELLE traduction hindi suit ces
   règles (हाउस jamais seul — qualifier selon le métier ; pas de गोथा,
   तमाशा, टेस्टिंग, हाउसफुल, कूचर, मोंदेन).
4bis. BACKFILL `iv` : fiches avec `iv` mais sans `iv_o` dans certaines langues
   de `tr` → traduire `iv_o/iv_g/iv_w` par lots de 10-15/passe, priorité fenêtre
   live la mieux notée. (`iv.c` jamais traduit.)
5. Chaque LUNDI : retester TOUS les liens (décompte au compte rendu) et
   régénérer le ld+json (60 meilleurs à venir).
6. Mettre à jour la date de l'eyebrow (« données collectées et vérifiées le
   JJ mois 2026 »).
7. Ré-injecter le JSON data (« </ » → « <\/ »), réécrire index.html.
7bis. `python3 tools/gen_seo.py AAAA-MM-JJ` puis `python3 tools/gen_pages.py`
   (pages indexables en AJOUT pur — index.html jamais modifié par gen_pages ;
   0 lien mort : chaque URL du sitemap doit avoir son fichier).
8. CONTRÔLES : `python3 tools/validate.py` (FAIL = ne pas pousser, corriger) ;
   `python3 tools/perfcheck.py` (0 régression) ; vérifier `git status`.
   `validate.py` BLOQUE aussi sur : jargon technique visible par l'internaute
   (un nom de champ du modèle, `None`, `TODO`… dans n/dt/ds/sw/p/pe/ci/ht/l/g/v)
   et sur un fichier `i18n-data/<lang>.json` dont les clés ne s'apparient plus
   aux fiches. Il SIGNALE (sans bloquer) les « &amp; » dans les traductions et
   les horaires restés à la française en ru/ar/hi/tr (« 20h30 » au lieu de
   « 20:00 » — contrôle volontairement limité à ces 4 langues : « 10h30 » est
   idiomatique en portugais).
9. PUBLIER (public) : `git add -A && git commit -m "V2 — maj JJ/MM" && git push`.
   Puis `bash tools/healthcheck.sh` (doit être OK ; sinon `tools/rollback.sh`
   et signaler).
10. Republier l'artifact : outil Artifact, file_path=<clone>/index.html,
    url=https://claude.ai/code/artifact/89b85688-ff57-481d-82d7-f7792051b066,
    favicon "⚜️", label "V2-maj-JJ-MM".
11. PUBLIER (privé) : commit+push du dépôt filet (journaux, .last-count,
    lessons.md, toute amélioration d'outil).
12. Compte rendu bref à Gérald : ajouts/purges/corrections, traductions,
    3-5 nouveautés glamour, événements des 48 h, KPI accès `iv`, résultats
    validate/healthcheck, confirmation adresse publique à jour, analyse des
    visites (voir ANALYSE DES VISITES ci-dessous), et toute anomalie (dont
    Search Console). Rien de neuf = une phrase.

## ANALYSE DES VISITES (directive du 28/07/2026)

Les statistiques du site sont publiques et anonymes (GoatCounter — jamais de
nom, d'adresse IP ni de cookie) :
  - tableau complet : https://constanceparis7.goatcounter.com/
  - compteur JSON : https://constanceparis7.goatcounter.com/counter/TOTAL.json
  - relevé quotidien : stats/visites.ndjson (une ligne par jour, écrite par
    tools/relever_visites.py — le lancer si le relevé du jour manque ;
    il refuse les doublons et ne bloque jamais si le compteur est illisible)
  - vitrine : https://constanceparis7.com/tableau-de-bord.html

À chaque passe, dans le compte rendu (étape 12) : 2 à 3 phrases de JOURNALISTE
sur les visites — progression depuis la veille, fiches qui attirent, pays et
sources qui montent (Instagram, Google), et tout croisement parlant
(« les visiteurs du Golfe arrivent sur les fiches de galas via Google »).
Statistiques illisibles = le dire en une phrase et passer ; ne JAMAIS bloquer
la passe pour une statistique, ne JAMAIS inventer un chiffre.

## AUTO-AMÉLIORATION PERPÉTUELLE (mandat permanent)

À chaque passe complète : un temps d'amélioration de la boucle, de la VITESSE
du site (mobile d'abord) et du référencement (Search Console = entrée de la
boucle, à corriger seul, à la source). Règle d'or : ne JAMAIS dégrader
l'expérience internaute ; alléger = charger moins, jamais montrer moins ;
ne JAMAIS fabriquer une donnée (prix, contact, date). Sûreté : mesurer avant
(perfcheck) → changer → mesurer après → publier si vert → rollback sinon.
CHANTIER PERF — **FAIT le 22/07/2026**, ne pas le refaire. Les 12 langues sont
différées : 3,82 Mo → 0,40 Mo gzip au premier affichage (9,5x plus léger),
13 langues vérifiées une à une, repli français en cas d'échec réseau confirmé.
Fonctionnement courant : voir « OÙ VIT LA VÉRITÉ » plus haut.

LEÇON À NE PAS REPERDRE : `split_i18n.py --apply` écrivait l'index allégé PUIS
copiait index.html vers index-full.html — il écrasait donc la version complète
et détruisait les 12 langues. Le bug était invisible en essai à blanc (dossier
de sortie séparé). Corrigé : la version complète s'écrit EN PREMIER, depuis le
HTML lu en mémoire, et un garde-fou refuse de finir si index-full.html n'est pas
strictement plus lourd que l'index allégé. Règle générale : un outil qui écrit
dans son propre dossier source doit toujours écrire la copie de sauvegarde avant
d'écraser l'original.

Prochains chantiers perf possibles : image hero en AVIF/WebP responsive,
et `loading="lazy"` sur les visuels hors écran.
