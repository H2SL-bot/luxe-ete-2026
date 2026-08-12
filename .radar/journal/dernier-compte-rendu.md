# Compte rendu — passe du 12 août 2026 (cloud, radar-routine-claude)

## Anomalie n°1 — accès réseau sortant bloqué pendant une bonne partie de la passe
`precheck.sh` signalait aussi une cadence rompue (15 h depuis le dernier run
journalisé) au démarrage — sans gravité : une session concurrente tournait déjà
et a publié pendant que je démarrais (voir plus bas).

Plus sérieux : pendant l'essentiel de la passe, **tout accès internet sortant
était refusé par la politique réseau de cette session** — y compris vers des
domaines témoins sans rapport (google.com, wikipedia.org), interrogés en même
temps que les liens à vérifier. Sur 27 liens d'événements des 7 prochains
jours testés (agents en arrière-plan, `WebFetch`) :
- **1 lot de 9 est passé sans problème** : 8 liens OK, 1 suspect (Grand Hotel
  Quisisana, Capri — le site existe et organise bien des galas, mais aucune
  page ne mentionne spécifiquement un dîner « Ferragosto » à vérifier une
  prochaine fois) ;
- **2 lots de 9 (18 liens) sont restés bloqués**, y compris après un
  deuxième essai — incident d'environnement, pas un verdict sur les fiches.
  À revérifier à la prochaine passe. Aucune fiche n'a été modifiée sur la
  seule foi de ce blocage.
- Conséquence directe : **aucune recherche de nouveaux événements ni aucun
  backfill séjour/invitation n'a pu être fait cette passe** — le travail
  aurait nécessité de vérifier des sources non accessibles, et la règle
  absolue du site (jamais de donnée non vérifiée) l'interdit.
Leçon consignée dans `.radar/tools/lessons.md`.

## Anomalie n°2 — une session concurrente était déjà active
Trois vagues de commits sont arrivées sur `main` pendant cette passe (une
juste avant mon premier push, deux pendant l'investigation), signées par une
autre session Claude (Opus 4.8) sous le même compte : fiches contrôlées,
retrait du Ritz Summer Bar (fermeture estivale confirmée par navigateur),
retrait du pop-up Dior à Shellona (collaboration non attestée), Grand Palais
d'été (saison de la Nef terminée). Rien d'anormal en soi — juste à signaler,
car deux passes actives en parallèle est justement le scénario que le verrou
`precheck.sh` est censé éviter. J'ai rebasé et poussé sans écraser ce travail.

## État général (après la dernière rebase, 465 fiches)
- `validate.py` : **OK — 0 blocker, 1 warning** (nouveau contrôle non
  bloquant ajouté cette passe, voir « Amélioration du filet » ci-dessous).
- `perfcheck.py` : **RÉGRESSION signalée — poids gzip 0,69 → 0,95 Mo (+38 %)
  alors que le site a 17 événements DE MOINS** que le dernier point enregistré.
  Cause identifiée sans avoir besoin du réseau (voir ci-dessous) : ce n'est
  pas moi qui l'ai causée, et je n'ai rien publié qui l'aggrave.
- Traductions manquantes : **0 / 465** (100 % traduit).
- Séjours manquants (hors fiches-conseil) : **188**.
- Invitations manquantes (`iv.o` vide) : **92**.
- Fiches sans lien officiel `u` : **10** (dont 2 dans les 7 prochains jours,
  cf. ci-dessous).
- KPI ACCÈS mondain (`iv`) : **271/323 (83 %)**.
- Adresse publique https://constanceparis7.com : **inchangée par cette
  passe** — je n'ai ajouté/modifié aucune fiche, donc rien à publier côté
  site public (voir raison réseau ci-dessus). Le site reflète les dernières
  publications de la session concurrente.

## Cause de la régression de performance — trouvée sans réseau
`iv.o` (le texte d'accès affiché au visiteur) a dérivé, sur des fiches
récemment « contrôlées », en journal d'enquête complet du contrôleur :
adresses vérifiées, hypothèses corrigées, citations de sources — jusqu'à
**4 891 caractères sur une seule fiche** (Capri / Anema e Core). Au total,
**115 fiches dépassent 1 200 caractères**, pour un excédent cumulé de
**158 453 caractères** par rapport à un texte visiteur raisonnable. Rien
d'inventé, tout est vérifié — mais ce n'est pas ce qu'un internaute doit lire,
et ça alourdit chaque page pour rien.

## Amélioration du filet (mandat d'auto-amélioration)
Ajouté à `validate.py` un contrôle **non bloquant** (WARN) : toute fiche dont
`iv.o` dépasse 1 200 caractères est signalée, avec l'excédent total. Non
bloquant pour ne pas geler la publication du jour — mais désormais visible à
chaque passe tant que ce n'est pas nettoyé. Prochaine étape suggérée (pas
faite cette passe pour ne pas entrer en conflit avec les fiches en cours de
contrôle par la session concurrente) : condenser chaque `iv.o` long à sa
conclusion + contacts vérifiés, garder le raisonnement hors du champ public.

## Analyse des visites
Compteur GoatCounter illisible aujourd'hui (réseau bloqué, `403` sur
`goatcounter.com`) — aucun chiffre inventé, relevé non écrit. D'après les 5
derniers jours déjà enregistrés (7→11 août) : progression régulière et
continue, 341 → 353 → 365 → 380 → 390 visites/jour (~+3 %/jour). Rien ne
permet de dire si la tendance s'est poursuivie le 12.

## Ce qui n'a PAS été fait cette passe (report)
Recherche de nouveaux événements, comblement de l'automne, nouveaux guides
d'accès, backfill séjours/invitations, traductions par lot : rien de tout
cela n'a pu être fait faute d'accès réseau vérifiable — et une session
concurrente y travaillait déjà pendant que je tournais. Priorité inchangée
pour la prochaine passe (ordre du 29/07 toujours valable) : séjours et
invitations manquants (188 / 92), puis automne, puis guides d'accès — plus,
si le réseau le permet, terminer la vérification des 18 liens restés
indéterminés cette fois.

## Traces
`git push` direct sur `main` accepté à chaque étape (après rebase sur les
commits concurrents). Aucun repli sur branche `claude/*` nécessaire.
