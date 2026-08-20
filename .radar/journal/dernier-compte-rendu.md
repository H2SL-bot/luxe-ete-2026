# Compte rendu — passe du 20 août 2026 (2e passe du jour, cloud, radar-routine-claude)

## Cadence
Deuxième passe du 20/08 : une passe complète avait déjà tourné plus tôt dans la journée
(condensation, 40 fiches). `precheck.sh` n'a signalé aucune anomalie — arbre propre,
verrou posé, `validate.py` vert au démarrage. La trace de démarrage a été poussée
directement sur `main` sans repli sur branche `claude/*`.

## PRIORITÉ DU JOUR — condensation des voies d'invitation (`iv.o`/`iv.g`/`iv.w`)

**20 fiches condensées et publiées**, toutes prises dans la fenêtre live et classées par
imminence, sélectionnées au seuil WARN réel de `validate.py` (un champ ≥ 1200 caractères,
la règle corrigée hier — le seuil de 400 caractères reste l'objectif de RÉDACTION, jamais
le critère de sélection).

- **Vague 1** (10 fiches) : Rina Banerjee (Espace Louis Vuitton Tokyo), Fondazione Prada,
  Villa Carmignac, Ron Mueck (Mori Art Museum × Fondation Cartier), Loro Piana × La
  Réserve à la Plage, Biennale Arte 2026, La Mode en majesté (Arts Décoratifs), Fondation
  Maeght (Peter Knapp), Le Jardin de Cheval Blanc Paris, Pop-up Vivrelle × Kith Women.
- **Vague 2** (10 fiches) : Loewe Paula's Ibiza (Saint-Tropez), Grand Palais d'été,
  Journey within (Ginza Maison Hermès), Van Cleef & Arpels (Galerie du Patrimoine), Into
  the Ocean (ArtScience Museum), Daniel Brush (L'École des Arts Joailliers), Dolce &
  Gabbana Beach Club (Gurney's Montauk), Picasso through the Eyes of Paul Smith, Yves
  Saint Laurent and Photography (ICP), L'Herbier Secret (Hôtel de Crillon).

**Volume retiré : environ 42 000 caractères de rapport d'enquête**, sans perdre un seul
contact. Aucun fait inventé, aucun fait vérifié supprimé.

### Résultat mesuré (`validate.py`, seuil WARN 1200 car.)
| | avant | après |
|---|---|---|
| fiches `iv.g` en excédent | 98 | **83** |
| excédent total `iv.g` | 71 057 car. | **61 678 car.** |
| fiches `iv.w` en excédent | 118 | **107** |
| excédent total `iv.w` | 114 170 car. | **102 563 car.** |
| `iv.o` | 0 WARN | **0 WARN** |

**Reliquat : 114 fiches en dérive réelle, dont 86 dans la fenêtre live** (contre 129 et
101 ce matin). À poursuivre par lots de 15-20 aux prochaines passes.

Cinq des vingt fiches condensées restent au-dessus de 1200 caractères sur un champ, et
c'est voulu : elles portent des grilles tarifaires complètes et plusieurs contacts
nominatifs (Yves Saint Laurent and Photography garde huit paliers d'adhésion, trois
jauges de privatisation et cinq intervenants nommés). La règle « garder le fait, couper
le reste » a été appliquée telle quelle.

## Un contrôle nouveau, et ce qu'il a trouvé
Les dix agents de la première vague ont tous affirmé n'avoir perdu aucun fait. Un
contrôle **algorithmique** écrit dans la foulée (extraction des e-mails, URLs, téléphones
et montants de l'entrée, puis différence avec la sortie sur la concaténation des trois
champs, puisqu'un fait peut légitimement migrer de `iv.o` vers `iv.w`) a montré le
contraire sur plusieurs fiches. Chaque écart a été instruit à la main :

- **Vraies pertes** : rattrapées avant publication.
- **Faux positifs de format** : « +33 (0)1 79 35 50 22 » et « +33179355022 » sont le même
  numéro, « 7,00 € » et « 7 € » le même tarif — la normalisation a été corrigée.
- **Suppressions légitimes, vérifiées une par une** : trois montants ont disparu à bon
  droit parce que la fiche elle-même les déclarait caducs — un tarif de 19 € « colporté
  par des sources secondaires et RÉFUTÉ » (Fondazione Prada), et une prévente japonaise
  close le 9 juin 2026 dont les tarifs en vigueur (2 400 / 1 400 / 1 000 ¥) sont bien
  conservés (Picasso × Paul Smith). Les republier aurait trompé le visiteur.

Le contrôle et ses trois pièges sont consignés dans `.radar/tools/lessons.md`.

## Registre `a-reverifier.md` remis d'aplomb
Le fichier avait atteint 706 lignes dont **73 répétitions du même en-tête** « Vérifiées à
moyens réduits », les mêmes fiches revenant jusqu'à quatre fois. Consolidé en une liste
unique de **147 doutes distincts**, chacun daté de son PREMIER signalement (l'ancienneté
du doute est l'information utile), plus une rubrique séparée pour le doute devenu sans
objet parce que la fiche a été purgée. 706 → 263 lignes, aucune information perdue,
toutes les sections narratives conservées.

## État de la LOI DU SITE
`reste.py` : traductions **433/433 (100 %)**, séjours 368/433, invitations 415/433.
Croisement avec `d2 ≥ aujourd'hui` : sur les **309 fiches non passées**, il manque
**0 séjour et 0 invitation**. Les 65 et 18 manquants sont tous des fiches déjà terminées,
gardées 30 jours avant purge et invisibles derrière le voile d'affichage. La fenêtre live
est donc à 100 % sur les deux portes.

## Recherche de nouveaux événements
Aucune, conformément à la consigne : la condensation passe avant la recherche de neuf
tant qu'il reste des fiches en dérive dans la fenêtre live — il en reste 86.

## Purge
Aucun zombie à purger aujourd'hui (le seul, l'exposition Pomellato, l'a été ce matin).
433 fiches, compte inchangé.

## Analyse des visites
1 795 visites le 20/08, contre 1 711 la veille : la progression continue mais se calme
nettement après cinq jours de flambée (426 → 458 → 478 → 631 → 1 046 → 1 711 → 1 795),
soit +5 % en un jour après un +64 % la veille. Le palier ressemble à une fin de vague
plutôt qu'à un décrochage. Aucun détail par page, par pays ou par source n'est
disponible : le tableau GoatCounter est injoignable depuis cette session (réseau bloqué,
voir ci-dessous). Le relevé du jour avait déjà été écrit par la passe du matin.

## Contrôles
- `validate.py` : **OK — 0 blocker, 2 warnings** (iv.g/iv.w, tous deux en baisse).
- `perfcheck.py` : **OK — 0 régression** (poids de la page en baisse de 0,02 Mo malgré
  20 fiches retouchées, effet direct de la condensation).
- Publication : 4 commits poussés **directement sur `main`** (démarrage, condensation
  vague 1, consolidation du registre, condensation vague 2). Aucun repli sur branche
  `claude/*` nécessaire. Adresse publique inchangée : https://constanceparis7.com

## Ce que je n'ai PAS pu vérifier
- **Réseau sortant bloqué**, comme aux passes des 11, 12, 13, 19 et 20/08 : `curl -sL`
  renvoie `000` sur des domaines témoins neutres (wikipedia.org, google.com) et le statut
  de la passerelle confirme `connect_rejected` — « gateway answered 403 to CONNECT ». Ce
  n'est donc pas un incident propre aux sites du radar. Conséquences du jour : **aucun
  test de lien**, aucune lecture de page officielle, aucun détail de fréquentation. La
  condensation, elle, n'en souffre pas : elle ne travaille que sur du texte déjà vérifié
  et publié, sans jamais rien ajouter.
- **Doublon toujours ouvert** : les deux fiches « DG Resort 2026 à Saint-Tropez — Casa
  Amor » et « Dolce & Gabbana x Casa Amor — takeover DG Resort » décrivent la même
  opération, mêmes dates, même lieu. Non fusionnées ici : un merge à 12 langues demande
  une relecture complète des deux jeux de traductions pour ne perdre aucun fait, et cela
  mérite une passe dédiée plutôt qu'une fin de session.
- **147 doutes de ré-audit** attendent toujours une passe avec réseau (registre
  consolidé aujourd'hui, mais aucun doute tranché faute de pouvoir lire une source).

## Anomalies
Une seule, à signaler franchement : un fichier d'agent est apparu entre le moment où j'ai
listé le lot et le moment où j'ai injecté, si bien qu'une fiche (Yves Saint Laurent and
Photography) est partie en ligne sans avoir passé le contrôle de préservation des faits.
Contrôlée immédiatement après publication : elle est saine, aucun fait perdu. La règle
qui en découle — n'ouvrir le contrôle qu'une fois TOUS les agents du lot rendus, un
fichier présent n'étant pas un fichier fini — est inscrite dans `lessons.md`.
