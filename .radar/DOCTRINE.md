# DOCTRINE DE LA PASSE — ConstanceParis7

> **Ce fichier fait autorité.** La routine cloud le lit à chaque exécution : il
> prime sur toute habitude générale et sur toute consigne plus ancienne.
> Pour faire évoluer la boucle, on modifie CE fichier et on pousse — aucune
> reconfiguration de la routine n'est nécessaire.
>
> Copie de référence : dépôt privé `H2SL-bot/luxe-radar-filet` (`PASSE.md`).

# PASSE.md — Doctrine complète du radar « French Luxury Events » (exécution CLOUD)

Vous mettez à jour « French Luxury Events », le radar PERPÉTUEL du luxe de la
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

## HORIZON ROULANT

- Couvrir en permanence AUJOURD'HUI → +90 JOURS.
- Suivre les SAISONS du circuit (été Riviera ; sept-oct Fashion Weeks, Voiles,
  Monaco Yacht Show, Art Basel Paris, Mostra ; hiver Courchevel/Gstaad/St-Barth/
  Miami ; printemps Cannes, GP Monaco, Met Gala…). Toujours sous filtre Riviera.
- PURGE à chaque passe complète : supprimer les événements d2 < aujourd'hui-30j
  (baisse de compte normale — l'indiquer au compte rendu).
- BRANDING : « ConstanceParis7 » (logotype capitales, 7 en or — NE JAMAIS
  TOUCHER). Ligne d'édition « French Luxury Events · Été 2026 ». Vers le 25 août,
  proposer à Gérald le rafraîchissement « Automne 2026 » — sans renommer seul.

## OÙ VIT LA VÉRITÉ — À LIRE AVANT TOUTE ÉDITION (bascule du 22/07/2026)

Depuis la bascule perf, le dépôt contient **trois artefacts** et il ne faut jamais
les confondre :

| Fichier | Rôle | Qui l'écrit |
|---|---|---|
| **`index-full.html`** | **SOURCE DE VÉRITÉ.** Document complet, les 12 langues embarquées dans `tr`. **C'est LUI qu'on lit et qu'on modifie.** | vous, à chaque passe |
| `index.html` | Ce que voit l'internaute : français seul + chargeur. ~9x plus léger (0,40 Mo gzip contre 3,82). **GÉNÉRÉ — ne jamais l'éditer à la main.** | `split_i18n.py` |
| `i18n-data/<lang>.json` | Une langue par fichier, chargée à la demande, indexée par clé stable « d1\|nom ». **GÉNÉRÉ.** | `split_i18n.py` |

**Conséquence pratique : lire et écrire `index-full.html`, puis lancer
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

## CADENCE — UNE PASSE PAR JOUR (7h Paris)

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

## PROCÉDURE — LA PASSE (matin, 7h03)

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
    validate/healthcheck, confirmation adresse publique à jour, et toute
    anomalie (dont Search Console). Rien de neuf = une phrase.

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
