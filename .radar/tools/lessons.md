# Journal d'apprentissage — International Luxury Events (boucle perpétuelle)

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

## 11/08/2026 — Un atelier d'agents peut mourir sans le dire
Deux ateliers de recherche (50 fiches chacun) se sont arrêtés à 12h30 sans erreur ni
notification ; je les ai crus vivants pendant 3 h. Aucun travail perdu (tout était
déjà publié ou en vérification), mais 3 h de production à zéro.
Filet permanent : la sonde `~/.radar-session/hb.sh` lit la DATE du dernier fichier écrit
par chaque atelier et affiche « ⚠️MORT(âge) » au-delà de 5 min sans écriture.
Règle : ne jamais juger un atelier vivant sur son compteur — un compteur figé
ressemble exactement à un atelier lent.

## 11/08/2026 — Un lieu FERMÉ produit un événement fantôme que rien ne détectait
Le site annonçait le « Réveillon du Nouvel An — Burj Al Arab, gala Al Muntaha »
du 31/12/2026, AVEC une voie d'invitation publiée. Or Jumeirah a fermé le Burj Al Arab
le 15/04/2026 pour 18 mois de restauration (réouverture visée octobre 2027) : toutes
ses tables sont à l'arrêt, la page d'Al Muntaha renvoie 404. Nous expliquions donc à
une lectrice comment se faire inviter à une soirée impossible — le pire cas pour la
crédibilité du site.
Ni la purge (date future, donc pas un zombie) ni validate.py (cohérence interne) ne
pouvaient le voir : le mensonge était dans le MONDE, pas dans le fichier.
Filet permanent : quand un vérificateur rend `fiable=false` au motif que le LIEU est
fermé/en travaux/définitivement clos, ce n'est pas le séjour qu'on saute — c'est
l'ÉVÉNEMENT qu'on retire, invitation comprise. Voir tools/lieux_fermes.md.
Réflexe de composition : vérifier l'OUVERTURE du lieu à la date de l'événement fait
désormais partie du prompt de recherche ET du prompt de vérification.

## 11/08/2026 — Un budget de recherche épuisé fabrique de faux doutes
En fin de session, les agents n'avaient plus de WebSearch (200/200). Plusieurs ont
conclu « aucune source officielle trouvée » — ce qui ressemble à s'y méprendre à
« l'événement n'existe pas », alors que c'est seulement « je n'ai pas pu chercher ».
Règle : ne JAMAIS retirer un contenu sur un agent privé de recherche. Le doute
s'inscrit dans `.radar/a-reverifier.md` et se tranche à la passe suivante.
Symétriquement : ne jamais PUBLIER non plus sur cette base. Un agent sans recherche
ne peut ni condamner ni absoudre.

## 11/08/2026 — Une limite de session tue les agents en vol : reprendre, pas relancer
À 16h09, la limite de session a coupé 29 agents sur 42 en plein travail
(V-SEJ-C : 10 aboutis / 10 tués ; V-INV-C : 3 / 19). Rien n'était perdu côté site,
car chaque fiche vérifiée était publiée AU FIL DE L'EAU — la règle a payé ce jour-là.
Deux réflexes à garder :
1. NE PAS relancer un atelier de zéro : `Workflow({scriptPath, resumeFromRunId})` rejoue
   les agents aboutis depuis le cache et ne refait travailler que les tués. Relancer à
   neuf, c'est repayer 10 vérifications déjà faites.
2. La sonde doit dire MORT, pas « lent ». Sans le marqueur d'âge de fichier ajouté le
   matin même, j'aurais attendu devant deux ateliers cadavres pendant une heure.
Corollaire de méthode : publier au fil de l'eau n'est pas une préférence de confort,
c'est ce qui rend une coupure indolore. Un lot gardé pour « publier à la fin » aurait
été perdu en entier.

## 11/08/2026 — Une source secondaire a fabriqué un tournoi entier
La fiche Deauville annonçait « Nouveauté 2026 : l'Asia Polo Cup (6-9 août) ouvre la
saison », avec une date de début au 6 août — et OMETTAIT la Coupe d'Or (17-30 août),
le tournoi le plus prestigieux du mois. Source invoquée : prensapolo.com, un média
secondaire. La page officielle du club, lue en direct, dit « BARRIÈRE DEAUVILLE POLO
CUP 2026 — 10 au 30 août » et ne mentionne aucune Asia Polo Cup.
Règle : quand une fiche cite une source secondaire À CÔTÉ de la source officielle
(champ `so` à deux URL), c'est le site de l'organisateur qui tranche, toujours.
Une « nouveauté » annoncée par un seul média et absente du site officiel est une
invention jusqu'à preuve du contraire.
Contrôle à ajouter à la routine : pour tout événement dont `so` contient une source
non officielle, rouvrir la page de l'organisateur et recouper dates ET intitulés.

## 11/08/2026 — Un renommage est indiscernable d'une perte de données
Corriger un titre faux fait disparaître l'ancien nom : le filet anti-perte a bloqué la
publication, à juste titre puisqu'il ne pouvait pas faire la différence. Or corriger un
titre est une opération légitime et fréquente — sans voie déclarée, la routine se
bloquerait elle-même chaque fois qu'elle rectifie un intitulé.
Filet : `.radar/renommages.json` ({avant, apres, date, motif}). L'ancien nom n'est
exempté QUE si le nouveau est présent dans les données du jour — c'est la preuve que la
fiche existe toujours. Motif vide = pas d'exemption.
Éprouvé dans les trois sens : sans déclaration → FAIL ; déclaré mais nouveau nom absent
→ FAIL explicite ; déclaration complète → OK.
PIÈGE DE TEST à ne pas répéter : validate.py réécrit `.last-names.json` à chaque succès.
Tester une disparition APRÈS un run réussi donne toujours OK — l'instantané a déjà
oublié l'ancien nom. Il faut remettre l'ancien nom dans l'instantané avant chaque test.

## 11/08/2026 — Un domaine perdu transforme une fiche en piège
La fiche Via Notte marquait « confirme » avec vianotte.com comme source ET comme lien
public. Or ce domaine n'appartient plus au club : il héberge un constructeur de maisons.
Chaque visiteur qui cliquait tombait sur un site sans rapport — et rien ne confirmait
la « saison 2026 » annoncée.
Contrôle à ajouter au filet quotidien : le vérificateur de liens doit alerter non
seulement sur les liens MORTS, mais sur les liens dont le CONTENU ne correspond plus
au sujet de la fiche (domaine racheté, parking SEO). Un lien qui répond 200 peut mentir.

## 11/08/2026 — Reprendre depuis le MAUVAIS identifiant refait tout en silence
En reprenant après la coupure de 22h, j'ai relancé le script des 18 séjours depuis
l'identifiant d'un autre atelier (celui de 5 fiches). Le harnais l'accepte sans broncher :
les clés de cache ne correspondant à rien, les 18 agents repartaient de zéro — dont 10
déjà faits. Aucune erreur affichée, juste le double du travail et du temps.
Règle : `resumeFromRunId` doit être l'identifiant de l'atelier qui a exécuté CE script,
pas un voisin. Vérifier avant reprise que le compteur d'aboutis de l'atelier correspond
bien à l'avancement attendu de ce lot.
Et tenir à jour le fichier d'étiquettes de la sonde : un libellé périmé m'a fait lire
« MORT » sur un atelier vivant et « vivant » sur un atelier mort. Un faux positif détruit
la confiance dans la sonde aussi sûrement qu'une alerte manquée.

## 11/08/2026 — Le dossier de travail temporaire s'efface ; les journaux d'agents, non
Le scratchpad a été vidé deux fois dans la journée, emportant les scripts d'ateliers.
Impossible alors de reprendre un atelier interrompu : `resumeFromRunId` exige le script.
Ce qui a sauvé la mise : les journaux d'agents, eux, persistent. `preparer_verif.py`
relit la RECHERCHE d'origine et régénère l'atelier de vérification en excluant tout ce
qui est déjà publié — il a reconstitué le reliquat exact (4 séjours, 13 invitations)
sans perdre une seule fiche.
Règles qui en découlent :
- les scripts d'appoint vivent dans `~/.radar-session/`, PAS dans le scratchpad ;
- ne jamais dépendre d'un fichier temporaire pour reprendre un travail ;
- toujours pouvoir régénérer un lot depuis sa source (le journal de recherche) plutôt
  que depuis un artefact intermédiaire.

## 12/08/2026 — `curl` sans `-L` fabrique de fausses réfutations
Pour trancher le conflit Alemagou, premier contrôle : trois URLs, trois réponses
`308`, `404`, `301`, et zéro mention d'Adriatique → j'ai failli conclure « réfuté ».
C'était faux : **sans `-L`, curl lit le corps de la redirection**, une page vide de
quelques octets, pas la page réelle. Le grep ne trouve rien parce qu'il n'y a rien
à trouver — pas parce que l'information est absente.

Refait avec `-L`, la réponse a changé de nature : `alemagou.gr` renvoie 200 avec
**138 Ko de contenu réel** et ne mentionne toujours pas Adriatique — là, l'absence
est une vraie information. Et `nightly.gr/en/venue/alemagou/` renvoie un vrai 404.

Règle : **toujours `curl -sL`, et toujours afficher la taille du corps récupéré.**
Une conclusion tirée d'une page de 0 octet n'est pas une conclusion. Corollaire :
un `406` (Songkick bloque les scripts) n'est PAS une réfutation, c'est un échec de
mesure — le dire au lieu de le compter comme une absence. Voir aussi la règle
« échec muet interdit ».

## 12/08/2026 — le 403 du Ritz : ouvrir un vrai navigateur au lieu de renoncer
Le contrôleur du « Ritz Summer Bar » a rendu un verdict honnête et inutilisable :
NON-VÉRIFIÉ, parce que ritzparis.com renvoie 403 à tout script et que les moteurs
opposaient un CAPTCHA. Il a eu raison de ne pas conclure — mais la fiche restait en
ligne, invérifiée, en annonçant une terrasse ouverte jusqu'au 12 septembre.

Repris avec l'outil navigateur (`preview_start` + `get_page_text`), le mur tombe en
douze secondes : le challenge anti-robot se résout tout seul et la page livre ses
11 338 caractères. Verdict immédiat et sans appel : « Summer Bar » absent du site,
et « Ritz Bar — Fermeture estivale du dimanche 9 août au 24 août ».

Règle : **un 403 / 406 / CAPTCHA n'est pas une conclusion, c'est une invitation à
changer d'outil.** L'ordre à suivre : curl -sL → navigateur → seulement alors,
déclarer l'échec. Un contrôleur qui rend NON-VÉRIFIÉ sur un 403 n'a pas fini le
travail ; c'est à la session principale de le reprendre au navigateur avant de
laisser une fiche invérifiée à la vue des visiteurs.

## 12/08/2026 — quand TOUT est bloqué, même google.com : ce n'est plus un lien mort, c'est l'environnement
Passe du matin (session cloud) : `curl -sL` direct échouait avec un 403 de la
passerelle d'egress dès le premier lien testé. Bascule vers WebFetch (agents en
arrière-plan, 3 lots de 9 liens) : le lot 2 est passé intégralement (8 OK, 1
suspect) ; les lots 1 et 3, RE-tentés une fois, ont échoué en bloc — y compris
sur des domaines témoins sans rapport (google.com, wikipedia.org) interrogés au
même instant. Ce n'était donc pas les 18 sites qui bloquaient : c'était la
politique réseau de CETTE session qui refusait le CONNECT vers ces hôtes-là,
pendant que d'autres passaient.

Règle : avant de conclure « lien mort » ou même « bloqué (anti-robot) », vérifier
si des domaines TÉMOINS sans rapport échouent au même moment (ou si un autre lot
lancé en parallèle passe, lui). Si oui, c'est un incident d'environnement, pas un
verdict sur les fiches — le dire explicitement au compte rendu, ne rien changer
aux fiches concernées, et prévoir de refaire la vérification à la prochaine passe.
Ne jamais insister en boucle (README de l'outil proxy : ne pas contourner un 403
de politique) — un seul nouvel essai suffit à distinguer panne passagère de
politique fixe.

## 12/08/2026 — `iv.o` a dérivé en journal d'enquête et a fait gonfler la page de +38 %
`perfcheck.py` a signalé une régression (poids gzip 0,69 → 0,96 Mo) alors que le
site avait 16 événements DE MOINS qu'au dernier point. Cause trouvée en local
(sans réseau) : le champ `iv.o` — un texte VISITEUR censé expliquer l'accès — est
devenu, sur 116 fiches « contrôlées » récemment, le compte rendu complet de
l'enquête du contrôleur (adresses vérifiées, hypothèses corrigées, citations de
sources, jusqu'à 4 891 caractères sur une seule fiche). Rien d'inventé, tout est
vrai et vérifié — mais ce n'est pas ce qu'un internaute doit lire pour savoir
comment être invité, et ça alourdit chaque page pour rien.
Filet ajouté (non bloquant, pour ne pas casser la publication du jour) :
`validate.py` avertit désormais au-delà de 1 200 caractères par `iv.o`, avec
l'excédent total. Reste à faire, à une prochaine passe qui ne touche pas déjà ces
fiches en concurrence : condenser chaque `iv.o` long à la CONCLUSION + contacts
vérifiés, en gardant le raisonnement détaillé hors du champ public (journal de
recherche, pas fiche visiteur).

## 12/08/2026 — un agent mort ne se signale pas : l'atelier reste ouvert pour rien
Le lot V-SEJ-G6 est resté bloqué à 11/12 pendant plus de deux heures. Le douzième
vérificateur avait cessé d'écrire à 09:33 UTC ; aucune erreur, aucun quota dépassé,
aucune notification — juste un agent qui ne rend jamais la main. L'atelier, lui,
restait « en cours » aux yeux du harnais, donc ni notification de fin ni récolte.

Signature à surveiller : **résultats < agents ET zéro fichier agent modifié depuis
plusieurs minutes**. C'est exactement ce que remonte la sonde (`actifs 0`) et il faut
le lire comme une mort, pas comme une pause.

Remède : `TaskStop({taskId})` puis `Workflow({scriptPath, resumeFromRunId})`. Les
agents terminés rejouent depuis le cache instantanément, seul le mort repart. Ne pas
attendre : deux heures d'attente n'ont rien débloqué.

## 13/08/2026 — précheck signalait une « cadence rompue » à CHAQUE passe depuis le 22/07
`precheck.sh` comparait l'écart depuis le dernier run à un seuil de 14 h, hérité de
l'époque « 2 passes/jour ». Le 22/07/2026, la passe du soir a été supprimée (décision
de Gérald) : la cadence nominale est devenue 1 passe/jour, avec un écart normal
d'environ 24 h entre deux passes. Un seuil de 14 h déclenche donc une fausse alerte
« CADENCE ROMPUE » à CHAQUE démarrage, y compris quand tout va bien — repéré ce jour
lors de la passe du 13/08 (écart réel : 23 h, aucune passe manquée).

Règle : un contrôle de seuil doit être révisé quand la cadence nominale qu'il
surveille change — sinon il devient du bruit permanent, et du bruit permanent fait
qu'on arrête de lire les vraies alertes. Corrigé : seuil relevé à 30 h (marge sur
les ~24 h nominaux, sans manquer un jour réellement sauté).

## 14/08/2026 — perfcheck confondait bloat et backfill séjour légitime
`perfcheck.py` comparait le poids gzip de la page au dernier point journalisé
(11/08 : 482 événements, 0,69 Mo) et bloquait tout poids >+20 % dès que le nombre
d'événements n'avait pas augmenté. Ce jour-là : 451 événements (purge normale) mais
1,08 Mo — +57 %, FAIL. Cause réelle : entre le 11/08 et le 14/08, le nombre de
fiches avec un séjour complet (`e.sej`, cœur de la LOI DU SITE) est passé de 257 à
325+ — le backfill séjour des passes précédentes avait fait grossir chaque fiche,
sans rien avoir à voir avec un bug. Le garde-fou ne distinguait pas « contenu voulu
qui pèse plus lourd » de « fuite ». Vérifié en comparant le index.html du commit du
11-12/08 (257 séjours, 0,92 Mo) au jour courant avant de conclure.
Corrigé : `perfcheck.py` journalise désormais `sej_count` et ne bloque le bloat que
si NI les événements NI les séjours n'ont progressé. Un vrai gonflement sans raison
reste attrapé ; une vague de séjours légitime ne bloque plus la publication.

Au passage, `validate.py` avait raison depuis le 11/08 (WARN : journal d'enquête
dans `iv.o` au lieu d'un texte visiteur, 132 fiches, 189 939 car. en trop) mais
personne n'avait encore condensé ces fiches — la WARN n'est pas bloquante et
personne ne l'avait traitée. 10 des pires fiches (>4 000 car. chacune) condensées
ce jour à la conclusion + contacts vérifiés (moins de 700 car. chacune), sans rien
inventer : tout vient du texte déjà vérifié. Reste 122 fiches à condenser — à
poursuivre par lots de 8-10 aux prochaines passes plutôt que de laisser le WARN
s'accumuler indéfiniment sans jamais être traité.
