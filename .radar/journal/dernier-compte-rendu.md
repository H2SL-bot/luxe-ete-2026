# Compte rendu — passe du 21 août 2026 (cloud, radar-routine-claude)

## Cadence
`precheck.sh` a signalé une **cadence rompue** : dernier run journalisé il y a 30 h
(seuil 30 h). Passe de RATTRAPAGE effectuée. Arbre propre au démarrage (aucun run
interrompu détecté). Trace de démarrage poussée directement sur `main`.

## Purge (zombies non purgés, bloquants)
2 fiches avec `d2` largement dépassé (2026-07-21, hors fenêtre de 30 j) empêchaient
la publication : **Festival d'Aix-en-Provence 2026** et **Belgium Day : La Maison
Rose — Nikki Beach**. Purgées. 432 → 430 événements.

## PRIORITÉ DU JOUR — condensation des voies d'invitation (`iv.o`/`iv.g`/`iv.w`)

**20 fiches condensées et publiées**, sélectionnées au seuil WARN de `validate.py`
(un champ ≥ 1200 caractères), prises dans la fenêtre live et classées par imminence
(date de début la plus proche en tête) :

Villa Carmignac (Sea, Pop & Sun), Biennale Arte 2026 (In Minor Keys), Fondation
Maeght (Peter Knapp — Le Temps Courrèges), Loewe pop-up Paula's Ibiza (Saint-Tropez),
Grand Palais d'été 2026, Journey Within (Maison Hermès Ginza), Van Cleef & Arpels
(Galerie du Patrimoine), Into the Ocean (ArtScience Museum × OceanX), Daniel Brush
(L'École des Arts Joailliers), Dolce & Gabbana Beach Club (Gurney's Montauk),
Picasso through the Eyes of Paul Smith, Yves Saint Laurent and Photography (ICP),
L'Herbier Secret (Hôtel de Crillon), Beach takeover Luisa Spagnoli (Capri), Givenchy
pop-up rue Gambetta, WE ARE [still] HERE (Petit Palais), Ellsworth Kelly (Fondation
Maeght), et 3 fiches-guide POINT D'ENTRÉE (Clienteling/VIC, Concierges Clefs d'Or,
Silencio).

**Méthode** : un agent par fiche (les lots échouent au-delà), consigne stricte
« aucun fait supprimé, seulement la forme », puis **contrôle mécanique** (regex
e-mails/URLs/téléphones/montants, entrée vs sortie) sur les 20 sorties avant toute
application aux données — pas de confiance sur la parole de l'agent (leçon du
20/08). Le contrôle a flagué 7/20 fiches ; examen au cas par cas :
- 4 fausses alertes pures (variations de format : `https://www.` tronqué, numéro
  de téléphone écrit avec/sans indicatif, montant `115,00 €` vs `115 €`, chemin
  d'URL raccourci sans perte de destination) ;
- 3 pertes réelles, corrigées avant publication : un e-mail « demandes non
  éditoriales » (Marina Bay Sands), un numéro de téléphone fusionné à tort avec un
  autre (Fondation Maeght), un e-mail de contact institutionnel (Les Clefs d'Or).

### Résultat mesuré (`validate.py`, seuil WARN 1200 car.)
| | avant (avec zombies) | après purge | après condensation |
|---|---|---|---|
| `iv.g` > 1200 car. | 91 fiches | 90 | **74** |
| `iv.w` > 1200 car. | 111 fiches | 110 | **97** |

Reste environ 74 fiches (`iv.g`) et 97 fiches (`iv.w`) à condenser — à poursuivre
par lots de 15-20 aux prochaines passes.

## LOI DU SITE — état sur la fenêtre live (306 fiches, aujourd'hui → +90j)
- Voie d'invitation manquante : **0**
- Séjour clé en main manquant (hors fiches-guide) : **0**
- Traductions 13 langues : **430/430 (100 %)**

Les compteurs globaux de `reste.py` (séjours 367/430, invitations 413/430)
concernent exclusivement des événements déjà passés, conservés 30 jours avant
purge — aucun manque réel côté visiteur.

## Contrôles
- `validate.py` : **OK — 0 blocker(s), 2 warning(s)** (le reliquat `iv.g`/`iv.w` ci-dessus).
- `perfcheck.py` : **OK — 0 régression**. Poids 1,04 Mo gzip (-0,02 Mo vs dernier
  point, -3 événements par la purge, -1 séjour).
- Publication : `bash .radar/session/publier.sh` — poussé directement sur `main`,
  aucun repli sur branche `claude/*` nécessaire.
- `healthcheck.sh` a expiré (timeout) — comportement déjà documenté (11/08, 12/08,
  19/08) : l'egress réseau est bloqué depuis cette session cloud. Confirmé ce jour
  sur des domaines témoins neutres (wikipedia.org, google.com : `curl -sL` → `000` ;
  `relever_visites.py` → `403 Forbidden` sur le tunnel). Ce n'est pas un signal sur
  l'état du site — le contrôle qui fait foi est `.github/workflows/surveillance.yml`.

## Recherche de nouveaux événements
**Non effectuée ce jour**, pour deux raisons cumulées : (1) la doctrine donne
priorité absolue à la condensation tant que la dérive « journal d'enquête »
n'est pas résorbée ; (2) le réseau sortant était bloqué en bloc pour cette
session (voir ci-dessus), ce qui aurait empêché toute vérification fiable de
nouveaux contacts ou dates.

## Analyse des visites
Impossible de relever le chiffre du jour (compteur GoatCounter injoignable,
réseau bloqué). Dernières données connues (`stats/visites.ndjson`) : 1 046 (18/08)
→ 1 711 (19/08) → 1 795 (20/08) — progression nette sur trois jours, sans donnée
fraîche pour confirmer la tendance du 21/08.

## Note d'architecture
`DOCTRINE.md` décrit encore un montage cloud à deux dépôts (`luxe-ete-2026` +
`luxe-radar-filet`) et une republication d'artifact Claude. Le dépôt réel de
cette passe est unique (`constanceparis7/radar-luxe`), conforme à `PASSATION.md`
(18/08/2026, transmission à Constance) — l'étape « republier l'artifact » de
la doctrine ne s'applique donc plus et a été omise sciemment. À signaler pour
mise à jour de `DOCTRINE.md` si elle doit rester la référence.

## À faire aux prochaines passes
- Poursuivre la condensation `iv` par lots de 15-20 (74 `iv.g` + 97 `iv.w` restants,
  probablement ~130-140 fiches distinctes en comptant le recoupement).
- Reprendre la recherche de nouveaux événements dès que le réseau sortant est
  disponible et que la condensation aura suffisamment reculé.
- Vérifier si `DOCTRINE.md` doit être réalignée sur l'architecture mono-dépôt.
