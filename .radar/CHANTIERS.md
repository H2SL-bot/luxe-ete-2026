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

**07 · La joaillerie est absente**
Fenêtre live : **92 festivals, 3 fiches de joaillerie.** Sur un radar du luxe
qui vise les maisons, c'est le déséquilibre le plus coûteux : c'est justement
la catégorie qui a des budgets et des attachés de presse.
Rappel des catégories : festival 92 · art de vivre 49 · sport 47 · mode 45 ·
art 40 · autre 22 · accès 10 · **joaillerie 3**.

**08 · Le radar s'éteint au printemps 2027**
janv. 15 · févr. 8 · mars 4 · **avril 0** · mai 4 · juin 1.
Un visiteur qui prépare un voyage en mars 2027 ne trouve rien. Ce sont les
mois où les grandes maisons publient déjà leurs dates.

**09 · Les 13 langues n'ont jamais été relues par un humain**
433 fiches × 12 langues traduites automatiquement. Personne n'a lu l'arabe, le
japonais, le hindi. Une seule tournure ridicule dans une langue, et le site perd
sa crédibilité auprès de ce public — sans que personne ne le signale jamais.
Priorité : les 12 accueils de langue, ce sont les pages vues en premier.

**10 · Neuf doublons possibles nom + ville**
Le doublon « Exposition Générale » a été trouvé le 20/08 : deux fiches pour la
même exposition, l'une annonçant des dates fausses. Huit autres paires portent
un nom et une ville proches. À trancher une par une — certaines sont peut-être
deux éditions légitimes.

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

**13 · Il n'existe aucune offre de partenariat**
La page « à propos » invite les maisons à écrire. Si l'une répond « que
proposez-vous ? », il n'y a rien à envoyer. À écrire : ce qui est vendu, à quel
prix, et ce qui ne se vend jamais (la place dans le radar).

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
