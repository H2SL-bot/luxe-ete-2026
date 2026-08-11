# Journal d'apprentissage — French Luxury Events (boucle perpétuelle)

Chaque incident ou erreur rencontré devient ici un **correctif permanent** : un
contrôle automatique dans le filet (`validate.py` / `healthcheck.sh` /
`perfcheck.py` / `precheck.sh`) qui empêche la même erreur de se reproduire.
C'est le moteur d'auto-amélioration : le filet grossit à chaque leçon.
Format : `AAAA-MM-JJ · symptôme → cause → correctif (outil)`.

## 2026-07-17

- **Run interrompu non commité.** `index.html` avait 66 traductions non commitées
  au démarrage (run de 01:02 stoppé avant `git commit`). → Détection au démarrage
  ajoutée : **`precheck.sh`** signale un index.html modifié non commité.

- **Deux passes concurrentes.** Une 2e passe a tourné en parallèle (mon commit
  425 puis un autre à 434 par-dessus). Ça a tenu par chance, mais deux passes
  peuvent se marcher dessus. → **Verrou de passe** dans `precheck.sh` (`.lock`,
  auto-expiration 90 min).

- **Healthcheck bernable.** Juste après un push, le live servait encore l'ancien
  build (16 juillet, 420 événements) mais `healthcheck.sh` disait OK via la
  tolérance « veille ». → **Contrôle de version** ajouté : le compte d'événements
  servi doit égaler `.last-count` (boucle de propagation intégrée).

- **KPI accès trop étroit.** Polo, voile, régate, concours d'élégance — très
  mondains — n'étaient pas comptés. → `MONDAIN_KW` élargi dans `validate.py`
  (KPI passé sur le vrai périmètre : 165/326).

- **Poids mobile lourd.** Transfert réel = 2,46 Mo gzip, dont 97 % dans le bloc
  data, dont ~2,1 Mo de traductions (10 langues qu'un internaute FR ne lit pas).
  Brotli non servi par GitHub Pages. → **`perfcheck.py`** (mesure + garde-fou de
  non-régression) et chantier « différer les 10 langues » (cible : 0,28 Mo,
  −88 %, ~8,5× plus léger au 1er chargement), à exécuter sous le harnais.

- **Traducteur qui échappe `&`.** Un agent a rendu `&amp;` dans des titres
  (« Arts &amp; Élégance »), contraire à la règle du site. → Nettoyage
  `&amp;`→`&` systématique à l'extraction/fusion des traductions.

## 2026-07-21

- **Search Console : champs recommandés manquants (Événements).** Google a signalé
  8 suggestions non critiques sur les données structurées (offers.price/
  priceCurrency/validFrom, organizer/organizer.url, performer, eventStatus,
  offers) — surtout issues des 512 pages e/*.html publiées le 17/07.
  → `gen_seo.py` + `gen_pages.py` enrichis : `offers` (url, availability,
  prix RÉEL parsé conservativement depuis e.p — jamais inventé ; 0 EUR pour le
  gratuit européen), `organizer.url`. `validFrom` et `performer` restent
  volontairement absents : les renseigner serait fabriquer une donnée.
  Contrôle permanent : parseur de prix testé unitairement (8 cas) avant patch.

- **Cron silencieux 4 jours (18-20/07), invisible.** Aucun contrôle ne détectait
  l'absence de passes ; le site est resté figé au 17/07 sans alerte.
  → Contrôle de CADENCE ajouté à `precheck.sh` : si le dernier run journalisé
  (run-log.ndjson) date de plus de 14 h, la passe s'annonce comme RATTRAPAGE
  et l'anomalie de déclenchement doit figurer au compte rendu.

## 2026-07-22

- **Passe du soir 21/07 manquée (cadence rompue, 17 h sans run).** Le contrôle
  de cadence ajouté la veille a fonctionné : `precheck.sh` a annoncé un
  RATTRAPAGE dès le début de passe. → Contrôle conservé ; l'anomalie de
  déclenchement figure au compte rendu.

- **Run interrompu avant commit (travail hi/tr en suspens).** `precheck.sh` a
  détecté index.html non commité ; le diff contenait 162 fiches traduites en
  hindi et turc, valides. → RÉFLEXE À GARDER : diagnostiquer le diff AVANT
  toute chose et le sécuriser par un commit dédié dès que `validate.py` passe,
  plutôt que de le laisser en suspens pendant toute la passe.

- **Corriger un champ FR invalide sa traduction.** En corrigeant des horaires
  vérifiés (Nice Jazz, Watermill, Ascot…), les `tr[lang][ht]` d'origine
  seraient restés faux dans 12 langues. → RÈGLE PERMANENTE : toute correction
  d'un champ français retire la clé correspondante dans chaque langue ;
  l'affichage retombe alors sur le français (exact) jusqu'à retraduction.
  Mieux vaut une ligne en français qu'un horaire faux traduit.

- **Chantier perf « différer les langues » : mécanisme prototypé et VALIDÉ en
  local, pas encore publié.** `tools/split_i18n.py` produit un index.html
  français seul (0,36 Mo gzip contre 2,92 Mo, soit -88 %, ~8x plus léger au
  premier affichage), un fichier par langue dans `i18n-data/`, et une copie
  intégrale `index-full.html` pour l'artifact Claude (page autonome : aucun
  fetch possible, donc elle doit rester complète). Vérifié sur serveur local :
  rendu FR immédiat, bascule russe et arabe (RTL) correctes, langue mémorisée
  rechargée au démarrage, repli sur le français si le fetch échoue.
  → Harnais mis à niveau AVANT la bascule : `validate.py`, `perfcheck.py` et
  `gen_pages.py` recollent désormais `i18n-data/*.json`, et `validate.py`
  BLOQUE si un fichier de langue est désaligné du bloc data (une seule fiche
  décalée afficherait la mauvaise traduction partout). Publication prévue à la
  passe complète suivante, en commit séparé, avec perfcheck avant/après.

- **Verrou de passe trop court : une 2e passe a commité en cours de route.**
  La passe du matin dure plus de 2 h (vagues de traduction) ; le verrou expirait
  à 90 min, si bien qu'une seconde passe a démarré à 09:20 et a poussé son propre
  commit (« Restaure 15 soirées vague 2 ») au milieu du travail.
  → Expiration du verrou portée à **4 h** dans `precheck.sh`.
  → Et surtout : la fusion des traductions ne fait plus confiance aux INDICES.
  Chaque lot rappelle le NOM français de la fiche visée ; si la fiche trouvée à
  cet indice porte un autre nom, le lot est ignoré au lieu d'écrire la traduction
  sur le mauvais événement. Même principe côté site pour le chantier perf : les
  fichiers `i18n-data/<lang>.json` sont indexés par clé stable « d1|nom », pas
  par position, donc ajouter ou retirer un événement ne décale plus rien.

- **Jargon technique visible par l'internaute.** Trois fiches affichaient des
  résidus de fabrication dans leur texte (« …dates variables, cf='probable' »,
  « d1/d2 = fenêtre de couverture du radar »), déjà traduits en 10 langues.
  → Contrôle BLOCKER ajouté à `validate.py` : tout champ lu par l'internaute
  (n, dt, ds, sw, p, pe, ci, ht, l, g, v) contenant un nom de champ du modèle
  (`cf=`, `d1=`…), `None`/`undefined`/`NaN`, `TODO`/`FIXME` ou `<script` fait
  échouer la validation. A trouvé les 3 cas dès sa première exécution.

- **Contrôle qualité des traductions.** `validate.py` signale désormais (WARN)
  les champs traduits contenant « &amp; » et, pour ru/ar/hi/tr uniquement, les
  horaires laissés à la française (« 20h30 » au lieu de « 20:00 »). Restreint à
  ces quatre langues à dessein : en portugais « 10h30 » est idiomatique — un
  contrôle trop large aurait produit 415 fausses alertes.

## 2026-07-22 (soir) — préparation de l'exécution 100 % cloud

Exigence de Gérald : la boucle doit tourner **Mac éteint**. Audit des dépendances
locales avant bascule ; trois défauts trouvés qui auraient cassé EN SILENCE dès
la première passe distante :

- **`date -v` est propre à macOS.** `healthcheck.sh` calculait la date française
  attendue avec `date -v-1d` : sous Linux la commande échoue, la date attendue
  devient vide, et la sonde de fraîcheur conclut n'importe quoi. → Repli en
  cascade `date -v` → `date -d` (GNU) → `python3`, testé dans les trois cas.
- **Le contrôle de cadence se serait auto-désactivé.** `precheck.sh` lisait
  l'horodatage du dernier run avec `date -j -f` (BSD) suivi de `|| echo 0`, ce
  qui, sous Linux, revenait à dire « pas d'écart de cadence » — le contrôle né de
  l'incident du 21/07 se serait tu exactement comme le cron qu'il surveille.
  → Même cascade de replis, et un message explicite si l'horodatage reste
  illisible. Leçon générale : **un repli `|| echo 0` sur une valeur de contrôle
  transforme une panne en silence.**
- **`healthcheck.sh` retombait en `MATCH="yes"` quand le compte de référence
  manquait** — or en cloud l'état repart d'un clone : ce cas devient fréquent.
  → Nouvel état `degrade` : le script sort en succès (le site va bien, pas de
  rollback intempestif) mais DIT que le contrôle de version n'a pas pu être fait.

- **`gen_pages.py` supprime des dossiers entiers sous `RADAR_REPO`.** Une variable
  d'environnement mal réglée à distance aurait effacé le contenu d'un autre
  dépôt. → `verifie_depot()` en tête : index.html présent ET `origin` contenant
  `luxe-ete-2026`, sinon refus d'agir. Testé sur un dépôt étranger et sur un
  dossier quelconque.

Mémoire de la boucle : dépôt privé `H2SL-bot/luxe-radar-filet` (doctrine
`PASSE.md`, marche à suivre `ROUTINE.md`, outils, journaux). `.lock` n'est jamais
versionné — un verrou commité bloquerait la passe suivante.

- **Le cron d'une routine cloud est en UTC.** Pour une boucle perpétuelle, c'est
  un piège : une routine réglée à 07:03 Paris en été se déclenchera à 06:03 en
  hiver. → Consigné dans `ROUTINE.md` §7 avec les deux tables de cron et la date
  de bascule (25/10/2026).
- **Création de routine par API : impossible sans `environment_id`.** Le schéma
  est reconstitué et documenté (`ROUTINE.md` §8), mais l'identifiant
  d'environnement ne peut pas être listé depuis une session. La création reste
  une opération d'interface — ce qui n'est pas gênant, les trois réglages
  indispensables (accès GitHub, pushes non restreints, réseau élargi) s'y font
  dans le même formulaire.

- **Deux passes ont bien tourné en parallèle toute la matinée du 22/07** (verrou
  expiré à 90 min sur une passe de plus de 2 h). Aucun dégât : les commits se sont
  empilés proprement et le garde-fou de fusion par NOM a évité toute traduction
  posée sur la mauvaise fiche. Mais c'est du travail fait deux fois — la bascule
  cloud doit s'accompagner de l'ARRÊT de la tâche locale, pas de sa cohabitation.
- **Limite de session atteinte en fin de vague** (5 lots de traduction sur 29
  perdus, reset à 12h). Comportement correct : la passe publie ce qui est prêt et
  inscrit le reste au backlog, plutôt que de tout retenir.

## 22/07/2026 — split_i18n --apply détruisait la version complète

SYMPTÔME : après `split_i18n.py --apply`, index.html ET index-full.html
faisaient tous deux 1,26 Mo. Les 12 langues de la version complète étaient
perdues (l'artifact autonome serait devenu monolingue).

CAUSE : l'outil écrivait l'index allégé dans index.html, PUIS faisait
`shutil.copyfile(src, index-full.html)` — or avec --apply, src EST index.html,
déjà écrasé. Il se copiait lui-même. Invisible en essai à blanc, où le dossier
de sortie est distinct de la source.

CORRECTIF : index-full.html est écrit EN PREMIER, à partir du HTML lu en
mémoire (jamais une copie de fichier) ; un garde-fou fait échouer l'outil si
index-full.html n'est pas strictement plus lourd que l'index allégé. La source
de vérité relue est désormais index-full.html quand il existe, ce qui rend
l'outil idempotent.

RÈGLE GÉNÉRALE : un outil qui écrit dans son propre dossier source doit écrire
la copie de sauvegarde AVANT d'écraser l'original, et vérifier après coup que
les deux diffèrent comme prévu.

## 28/07/2026 — la preuve est tombée, avec six jours de retard

Le commit du test cloud du 22/07 (auteur « radar cloud », horodaté
22/07 12:21:07, soit 70 secondes après le lancement) est apparu sur main
le 28/07 vers 12:30. CE QUE ÇA PROUVE, définitivement :
  1. une session cloud PEUT cloner le dépôt → l'accès GitHub fonctionne ;
  2. une session cloud PEUT pousser DIRECTEMENT SUR MAIN → la permission
     de publication fonctionne (aucune branche claude/*, aucun report).
Les deux blocages redoutés n'existent pas. La configuration est bonne.

CE QUE ÇA RÉVÈLE : l'exécution des sessions cloud peut être retardée ou
livrée TRÈS tardivement (ici ~6 jours). Un silence n'est donc pas une
preuve d'échec — c'est pour cela que la trace de démarrage désormais
imposée par le prompt est précieuse : elle date le vrai passage.

CAUSE RESTANTE DES SILENCES DU 22/07 : les sessions lancées pendant les
périodes de quota épuisé meurent sans trace. Le test qui a réussi (12:21)
est parti UNE MINUTE après la réinitialisation de midi. Conclusion
pratique : la passe de 7h03 doit partir sur un quota frais — éviter de
vider le quota du compte par de gros travaux la veille au soir.

## 28/07/2026 — passe cloud : trois leçons

1. **`gen_seo.py --help` corrompait le sitemap.** L'outil prenait argv[1] tel
   quel comme date : « --help » est parti dans les 6172 <lastmod> du sitemap.
   Détecté par relecture immédiate, corrigé en relançant avec la vraie date.
   FILET : gen_seo.py refuse désormais tout argument non conforme à AAAA-MM-JJ.

2. **Quota de session : 2 lots de traduction sur 4 perdus** (it/de/ru et
   ko/hi/tr, « session limit, resets 15:00 UTC »). Comportement doctrine
   appliqué : publier les 6 langues prêtes (en/es/pt/ar/zh/ja), backlog pour
   les 6 autres. À la prochaine passe : reprendre le backfill iv des fiches
   332, 347, 198, 286, 265, 208, 228, 235, 200, 216, 231, 245 en it/de/ru/
   ko/hi/tr (source française dans iv de chaque fiche).

3. **Push concurrent pendant la passe.** Gérald a poussé le chantier
   « mesure d'audience » (mouchard GoatCounter dans le gabarit gen_pages)
   pendant que la passe tournait : push refusé, 369 conflits sur pages
   GÉNÉRÉES uniquement. Résolution sûre : prendre LEUR version des outils et
   des pages, puis relancer gen_pages.py avec le NOUVEAU gabarit — les pages
   repartent des données à jour ET gardent le mouchard. Règle : après toute
   fusion, TOUJOURS régénérer les pages avec le gen_pages.py fusionné avant
   de pousser, sinon on publie des pages sans le dernier gabarit.

4. **healthcheck.sh est aveugle depuis une session cloud** : l'egress réseau y
   est bloqué (http=000000 dans run-log, à ne pas confondre avec un site KO).
   NE PAS déclencher rollback.sh sur un échec « 000 » venu d'une session
   cloud : c'est la sonde qui n'a pas de réseau, pas le site qui est tombé.
   Le vrai contrôle en ligne est .github/workflows/surveillance.yml (2x/jour,
   avec réseau, ouvre une issue si le site est périmé ou KO) — c'est lui qui
   fait foi. Preuves du jour : plancher 10:32 UTC = 200/470/date fraîche.

5. **Fusion pendant travail long (bis, 28/07 soir)** : pendant le backfill des
   24 fiches, main a reçu le « voile d'affichage » (index.html modifié).
   Piège évité : index-full.html reconstruit AVANT la fusion aurait écrasé ce
   changement au split. Procédure sûre appliquée : merge → rebuild_full.py
   depuis l'index.html fusionné → ré-injection des traductions (scripts et
   sources conservés dans le scratchpad, ré-exécution idempotente) → split.
   Règle : TOUJOURS git fetch + merge AVANT split_i18n --apply, et garder les
   données d'injection re-jouables tant que la passe n'est pas poussée.

## 2026-07-29

1. **`.radar/tools/.lock` candidat à un commit.** Le hook de fin de session a
   signalé ce fichier comme non suivi. C'est un verrou purement local
   (anti-concurrence de `precheck.sh`) : il ne doit jamais être versionné.
   FILET : ajouté à `.gitignore`.

2. **Renommer une fiche (correction factuelle du nom) déclenche un faux
   blocage `validate.py`.** Correction du 21/07 : « Festival de Ramatuelle —
   42e édition » était faux (le festival fêtait son 40e anniversaire en 2025,
   2026 = 41e). En renommant la fiche, `validate.py` a cru à une perte de
   données (son contrôle « fiche non périmée disparue » compare par NOM à
   `tools/.last-names.json`, écrit uniquement lors d'un run OK précédent).
   Correctif appliqué : mise à jour manuelle de la clé dans
   `.last-names.json` (même `d2`, nouveau nom) avant de relancer `validate.py`.
   RÈGLE : tout renommage volontaire et sourcé d'une fiche existante doit
   être répercuté dans `.last-names.json` dans la même passe, sinon la
   publication reste bloquée à tort.

3. **Deux nouvelles fiches nées sans `sej`.** En composant les fiches Villa
   Ephrussi et Lisa Stansfield, le séjour (`sej`) a été oublié à la première
   écriture — seul `iv` avait été rempli. Rattrapé avant traduction/publication
   grâce à la relecture systématique du JSON source avant de lancer les agents
   de traduction. RÈGLE : lors de la création d'une fiche, vérifier la
   présence de `iv` ET `sej` ensemble avant de considérer la fiche « complète »
   (LOI DU SITE) — ne pas se fier à la mémoire du prompt initial.

## 29/07/2026 — Google explorait sans indexer : les pages taisaient la valeur
Search Console : « Explorée, actuellement non indexée » + « page en double ».
Le technique était BON (canoniques auto-référencées, hreflang complet,
redirections http→https et www→non-www normales — ces deux dernières expliquent
à elles seules le motif « Page avec redirection », il n'y a rien à corriger).
La vraie cause était le CONTENU : les pages générées faisaient 154 mots parce
qu'elles ne publiaient ni le séjour clé en main ni — en français — la voie
d'invitation. Deux bugs :
  1. `T(e, "fr", "iv_o")` renvoyait None : en français la donnée vit dans
     `e["iv"]["o"]`, pas dans un champ plat. Toutes les pages FR étaient donc
     amputées de la raison d'être du site.
  2. Le bloc `sej` n'était tout simplement pas rendu.
Corrigé : 154 → 487 mots sur la fiche témoin, médiane 169 → 260, 141 pages
enrichies. CONTRÔLE PERMANENT ajouté à validate.py : il apparie chaque page à
sa fiche PAR LE <h1> (jamais en devinant le slug — la règle de nommage
appartient à gen_pages.py) et BLOQUE si le séjour ou l'accès manque.
Deux pièges rencontrés en l'écrivant, à ne pas reperdre :
  - deviner le nom de fichier = 0 page retrouvée, garde-fou muet et inutile ;
  - comparer sans décoder les entités HTML (`&` vs `&amp;`) = fausses alertes.
Testé dans les deux sens : sabotage du gabarit → BLOCK, gabarit sain → OK.

## 04/08/2026 — perfcheck bloquait la routine chaque fois qu'elle purgeait
Après une semaine d'absence, la publication a été refusée : « perte de contenu
537 -> 532 événements ». Or ces cinq disparitions étaient des PURGES normales
(événements terminés depuis plus de 30 jours), quatre par le plancher pendant
la semaine, une par moi. La règle « toute baisse = blocage » condamnait donc la
routine à échouer chaque fois qu'elle faisait correctement son travail — et
elle exécute perfcheck à chaque passe (doctrine étape 8).
La vraie perte de contenu était DÉJÀ couverte, et mieux, par validate.py : son
garde anti-suppression bloque si une fiche NON EXPIRÉE disparaît
(.last-names.json). La règle de perfcheck était redondante et fausse.
Corrigé : perfcheck ne bloque plus que sur une chute de plus de 15 %, qu'aucune
purge normale ne peut expliquer. Testé dans les deux sens — 532 -> 300 (-43 %)
déclenche bien le blocage, la purge de cinq fiches passe.
RÈGLE GÉNÉRALE : un garde-fou qui punit le fonctionnement normal finit par être
contourné ou neutralisé. Avant d'écrire un contrôle, se demander « qu'est-ce que
la machine fait légitimement tous les jours ? » et ne bloquer que l'anormal.

## 05/08/2026 — un gros lot affame ses propres vérificateurs
Vagues de 50 événements en pipeline recherche→vérification : au bout de 28
minutes, 22 recherches abouties et ZÉRO vérification. Cause : la concurrence
est plafonnée à 16 agents simultanés, et 50 recherches en attente occupent
toutes les places. Les vérificateurs ne démarrent jamais — donc rien n'est
publiable, et une limite de session ferait tout perdre.
RÈGLE : soit des lots de 8-10 (la recherche libère vite des places), soit —
mieux — SÉPARER les deux étapes en deux workflows distincts : un qui cherche
en continu, un qui vérifie ce qui est déjà cherché. Chacun dispose alors de
toute la concurrence, et on publie au fil de l'eau.
Corollaire : toujours vérifier « combien de VÉRIFICATEURS ont démarré », pas
seulement « combien d'agents tournent » — grep 'ADVERSARIALE' sur les
transcripts le dit en une seconde.

## 11/08/2026 — WebFetch bloqué en session cloud + un contact halluciné intercepté de justesse

1. **`WebFetch` renvoie systématiquement `EGRESS_BLOCKED`** dans cette session
   cloud, sur tous les domaines testés (constanceparis7.com, artbasel.com,
   wikipedia.org) — `WebSearch` fonctionne, lui, normalement. Contrairement au
   blocage réseau documenté les 28-29/07 et le 05/08 (qui touchait `curl` et
   `healthcheck.sh`), celui-ci touche aussi la recherche web profonde par
   fetch de page. RÈGLE : quand `WebFetch` échoue sur un domaine neutre
   (wikipedia.org) dès le début de passe, ne pas s'acharner — informer les
   agents de recherche qu'ils doivent travailler uniquement avec `WebSearch`
   (extraits + sources), et rester en conséquence plus prudent sur la
   profondeur de vérification atteignable (voir leçon suivante).

2. **Un agent de recherche a produit un contact totalement plausible mais
   FAUX** : "Audrey Le Véziel — Responsable Communication, Événementiel et
   Sportif, Le Touquet Golf Resort" + email `aleveziel@resonance.golf`, sur
   la seule foi d'un résumé généré par l'outil de recherche (pas d'extrait
   source brut). Un agent vérificateur adversarial dédié, lancé ensuite pour
   contre-vérifier CE nom précis, a trouvé un profil LinkedIn indépendant
   pour ce nom exact rattaché à un métier totalement différent (chef de
   rang en restauration) — signal fort de fabrication ou de confusion
   d'homonyme. Le contact a été écarté avant publication ; les deux autres
   noms de la même vague (Héléna Dupuy/France Galop, Charles Debruyne/Touquet)
   ont été confirmés par LinkedIn indépendant sur le nom et la fonction, mais
   PAS sur le téléphone/email associé (visibles seulement dans les résumés de
   l'outil, jamais dans un extrait source brut) — ces coordonnées non
   confirmées ont été retirées, seuls le nom et la fonction corroborés ont
   été publiés, avec les contacts génériques déjà connus en repli.
   RÈGLE PERMANENTE : quand `WebFetch` est indisponible et que la recherche
   ne repose que sur des résumés `WebSearch`, TOUJOURS faire vérifier par un
   second agent, dont le seul mandat est de réfuter, tout nom propre associé
   à un téléphone ou un email avant de le publier — un nom+fonction corroboré
   par une source indépendante (ex. LinkedIn) ne rend pas automatiquement
   vraies les coordonnées qui l'accompagnaient dans la première réponse. En
   cas de doute sur une coordonnée précise (numéro, email) même quand le nom
   est confirmé : la retirer et garder uniquement le contact générique publié.

## 11/08/2026 — `validate.py | tail` masque son propre échec
`python3 validate.py 2>&1 | tail -1 && git commit && git push` publie TOUJOURS :
dans un tuyau, le code de sortie retenu est celui de `tail`, pas celui de validate.
J'ai ainsi commité un état à 45 blocages. Filet permanent : `~/.radar-session/publier.sh`
teste le TEXTE de la dernière ligne (`case "$V" in OK*)`) et sort en erreur sinon.
Règle : ne jamais enchaîner une garde derrière un tuyau.

## 11/08/2026 — Base locale périmée = faux blocages en cascade
Les 45 blocages ne venaient pas du contenu mais d'un `index-full.html` vieux de 6 jours,
sur lequel j'avais injecté. Réflexe obligatoire avant toute injection après une pause :
`git fetch && git reset --hard origin/main && rebuild_full.py`, PUIS injecter.
