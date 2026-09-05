# Compte rendu — passe du 05/09/2026

## Priorité du moment : condensation des voies d'invitation

16 fiches condensées (tout le stock au-dessus du seuil WARN de 1200 caractères sur `iv.o`/`iv.g`/
`iv.w`, toutes dans la fenêtre live sauf 2) : Villa Carmignac, Biennale Arte 2026, Yves Saint
Laurent and Photography, POINT D'ENTRÉE (ventes aux enchères), Armani/Silos, Dior Spa Cheval Blanc,
Grand Hôtel de Cala Rossa, Hôtel & Spa des Pêcheurs, Scene yacht Ibiza-Formentera, Dubai Racing
Carnival, Saint-Barth Cata Cup, Formula 1 Abu Dhabi GP, Gstaad New Year Music Festival, St Barth
Music Festival, Cavo Paradiso, Black Coffee Residency. Méthode : un agent par fiche, puis contrôle
mécanique `verif_faits.py` (entrée vs sortie) sur les 16 — les quelques alertes levées étaient soit
des suppressions légitimes déjà signalées comme fausses/périmées dans le texte source, soit des
faux positifs de format (montants sans € répété dans une liste). Aucune perte réelle de fait dur.

**Reliquat** : après condensation, il ne reste que des fiches légitimement denses au-dessus du
seuil (plusieurs contacts/tarifs distincts qu'on ne peut pas couper sans perdre un fait — POINT
D'ENTRÉE et Abu Dhabi GP). Le défaut « journal d'enquête » signalé le 12-19/08 est traité.

## Naissance complète des 8 ancres printemps 2027 (LOI DU SITE)

Les 8 ancres identifiées le 22/08 (TEFAF Maastricht, Watches and Wonders Geneva, Salone del Mobile
Milano 65e, Fuorisalone, Festival de Cannes 80e, GemGenève, Grand Prix de Monaco, Royal Ascot)
existaient sans `iv` ni `sej`. Composées aujourd'hui par recherche web réelle, puis **vérifiées par
8 agents adverses indépendants** : 6 corrections réelles trouvées et appliquées avant publication
— 2 URLs mortes (Bayview/W&W, 10 Corso Como/Fuorisalone), 3 violations du garde-fou coordonnées
personnelles (voir leçon ajoutée à `lessons.md`), 1 tarif faux (Royal Ascot Queen Anne : 264£ →
85-125£ réel), 1 numéro de téléphone erroné attribué à la mauvaise personne (TEFAF). Puis traduites
en 12 langues (agents parallèles, un par langue). Complété aussi le 66e International Red Cross
Ball, qui avait des contacts RSVP réels mais aucun texte de synthèse `iv.o/g/w` — rédigé à partir
de ses propres données déjà vérifiées, sans rien ajouter.

**Résultat : fenêtre live (aujourd'hui → +90j, 290 fiches) à 0 séjour manquant et 0 invitation
manquante — LOI DU SITE honorée à 100 % sur ce qui est réellement montré aux visiteurs.**

## Purge et liens

- 1 zombie purgé (Délices Sonores, fin 05/08, franchi le seuil des 30 jours aujourd'hui même —
  vérifié : ce n'est pas une panne du plancher automatique, la fenêtre de purge venait de s'ouvrir).
- 4 liens morts détectés par la passe automatique et confirmés par `curl -sL` (corps + titre de
  page), tous sur des événements EN COURS dans la fenêtre live : Petit Palais (mauvais chemin,
  corrigé vers `/en/we-are-still-here`), Hôtel de Crillon (URL de communiqué expirée, redirigée
  vers la page hôtel), Bagatelle Bodrum (article de presse tiers mort, redirigé vers le site
  officiel), Verde Beach (page ligne-up morte, redirigée vers l'accueil du site). Corrigés et
  republiés.
- 119 liens testés au total par la passe automatique du matin, aucune autre casse.

## Chiffres (recomptés, fenêtre live = aujourd'hui → +90j)

| | avant la passe | après la passe |
|---|---|---|
| Traductions manquantes (13 langues) | 0 | 0 |
| Séjours manquants (fenêtre live) | 8 | **0** |
| Invitations manquantes (fenêtre live) | 9 | **0** |
| Événements publiés | 396 | 395 (1 zombie purgé, 0 ajout net — pas de recherche de nouveaux
événements aujourd'hui, priorité donnée à la condensation et au rattrapage LOI DU SITE) |
| KPI accès mondain (`iv`) | 262/267 (98%) | 266/267 (99%) |

## Ce qui n'a pas pu être vérifié / reste en suspens

- La 66e édition du Red Cross Ball et sa date (08/01/2027) restent une **extrapolation non
  confirmée officiellement** (déjà noté dans `dt` de la fiche) — à reconfirmer auprès du chapitre
  Floride du Sud avant la saison.
- Le Grand Prix de Monaco 2027 reste **sous réserve d'approbation FIA** (statut confirmé encore
  valide par le contrôleur adverse aujourd'hui) — à revérifier sur acm.mc à chaque passe tant que
  le calendrier F1 2027 définitif n'est pas publié.
- Traductions de la correction du Red Cross Ball (iv.o/g/w nouvellement écrits) : laissées en
  français dans les 12 langues pour l'instant (repli documenté et sûr) — à traduire à une prochaine
  passe, volume trop mineur pour justifier 12 agents ce jour.
- Pas de recherche de nouveaux événements aujourd'hui : la journée a été consacrée en totalité à la
  priorité de condensation puis au rattrapage LOI DU SITE des 8 ancres, comme la doctrine le prescrit
  quand ces chantiers ont un reliquat.
- Analyse des visites : 2519 visiteurs/pages vues aujourd'hui, en progression régulière depuis 5
  jours (2427 → 2519, +3,8 %). Pas de recoupement pays/source fait aujourd'hui (temps consacré au
  rattrapage LOI DU SITE) — à reprendre à la prochaine passe.
- Branding de saison : toujours « Été » au 05/09 alors que le rafraîchissement « Automne » aurait
  dû être proposé vers le 25/08 (déjà signalé par les passes précédentes) — décision toujours en
  attente de qui de droit (Constance, depuis la passation du 18/08), pas prise seul.

## Contrôles

`validate.py` : 0 blocage, 3 avertissements (2 `iv` légitimement denses au-dessus de 1200
caractères, 1 rappel de saison). `coherence_i18n.py` : OK, aucune divergence. `healthcheck.sh` :
OK (http=200, compte live=395=attendu, date fraîche). Publication faite en 5 commits successifs au
fil de l'eau, tous directement sur `main` (aucun repli de branche nécessaire aujourd'hui).

## Leçon ajoutée à `lessons.md`

« Un renvoi vers une page de contact peut réintroduire une coordonnée personnelle sans la citer » —
le garde-fou de protection des personnes porte sur l'intention (ne pas conduire le lecteur vers une
coordonnée personnelle), pas seulement sur la présence littérale d'un numéro/email dans le champ.
Complète aussi la liste des formats interdits (`prenom.nom@` et `initiale+nom@`, quel que soit le
domaine, corporate compris) et ajoute un cas nouveau : une attribution nominative non confirmée
pour l'édition en cours d'un événement futur est un risque du même ordre qu'un contact inventé.
