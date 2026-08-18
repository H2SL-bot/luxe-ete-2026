# Passation — ConstanceParis7, International Luxury Events

*Écrit le 18 août 2026, jour de la transmission de Gérald à Constance.*

Bienvenue, Constance. Ce site est désormais le tien. Voici tout ce qu'il faut
savoir pour le tenir — rien n'est caché ailleurs : ce document, la doctrine et
les registres du dossier `.radar/` contiennent la totalité de la mémoire du site.

## Ce qu'est le site

Un radar mondial d'événements de luxe (constanceparis7.com), 13 langues, dont la
raison d'être tient en deux promesses : **tout ce qui est affiché est vrai**, et
pour chaque événement le site apporte **la voie d'invitation** (comment être
invité, la personne par qui l'accès passe) et **le séjour clé en main** (palaces,
tables, expériences — tous vérifiés). Au jour de la passation : 437 fiches,
100 % des événements à venir couverts en séjours et invitations, 300+ événements
archivés, validation 0 blocage / 0 avertissement.

## L'architecture en une minute

- **Une seule page** `index.html`, générée depuis `index-full.html` (la source de
  vérité, avec toutes les traductions) par `.radar/tools/split_i18n.py` — les
  langues sont servies en différé (`i18n-data/*.json`) pour la vitesse mobile.
- `evenements.html` + ~7 000 pages par langue/événement : générées par
  `.radar/tools/gen_pages.py` pour Google. `archives.json` : la mémoire, chargée
  à l'ouverture de la rubrique Archives.
- **Hébergement** : GitHub Pages, domaine via le fichier `CNAME`. Pousser sur
  `main` = publier. Il n'y a pas d'autre déploiement.

## Les deux règles au-dessus de tout

1. **Jamais publier sans le filet.** `.radar/session/publier.sh` est l'unique
   porte de sortie : il exécute `validate.py`, qui REFUSE de pousser au moindre
   blocage (JSON cassé, zombie non purgé, divergence de traduction, fuite
   technique dans un texte visiteur...). Ne jamais faire `git push` à la main.
2. **Au moindre doute, on retient ou on retire.** Un événement douteux ne reste
   pas en ligne. Tout retrait se déclare dans
   `.radar/retraits-volontaires.json` avec son motif, tout renommage dans
   `.radar/renommages.json` — sinon le filet croit à une perte de données et bloque.

## Ce qui tourne tout seul (GitHub Actions — rien à faire)

- `passe-quotidienne.yml` (8h40 Paris) : purge des événements finis depuis plus
  de 30 jours, bascule de saison du titre (équinoxes/solstices, automatique),
  test des liens les plus imminents.
- `surveillance.yml` et `bulletin-quotidien.yml` : santé et compte rendu.
- Aucun secret, aucune clé : les workflows sont autonomes.

## Ce que TU fais avec Claude (ton compte Claude Pro suffit)

Installe Claude Code, clone le dépôt, et ouvre une session dans le dossier.
Dis-lui de lire `.radar/PASSATION.md` et `.radar/DOCTRINE.md` d'abord. Ensuite :
- **Ajouter des événements** : Claude cherche, compose, puis fait VÉRIFIER par
  des agents adverses (gabarits dans `.radar/session/gabarits/`) avant d'injecter.
- **Corriger** : toujours vérifier à la source AVANT de toucher au site, dans un
  vrai navigateur si un site bloque les scripts (les leçons durement apprises
  sont dans `.radar/tools/lessons.md` — lis-les, elles valent de l'or).
- **Publier** : `bash .radar/session/publier.sh "message"` — au fil de l'eau,
  jamais en fin de chantier.

## Les pièges connus (résumé de lessons.md)

- Un HTTP 200 peut cacher un 404 ; un 403/CAPTCHA n'est PAS une preuve d'absence.
- Les sites de luxe se lisent souvent au NAVIGATEUR, pas en script.
- Corriger le français n'invalide pas les traductions : le filet
  `coherence_i18n.py` bloque si un mois diverge entre langues.
- Un contrôleur qui dit « cet événement n'existe pas » se vérifie comme le reste.

## Contacts techniques du site

- Domaine : Gandi (transféré à ton nom — voir avec Papa la date effective).
- Statistiques : GoatCounter (constanceparis7.goatcounter.com).
- Référencement : Google Search Console, propriété constanceparis7.com — tu en
  es propriétaire ; le sitemap est soumis, n'y touche pas sans raison.

Le site est exigeant sur un seul point : la vérité de ce qui est affiché.
Tout le reste n'est que de l'outillage. Bonne route. 🤍
