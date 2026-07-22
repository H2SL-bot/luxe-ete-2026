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
