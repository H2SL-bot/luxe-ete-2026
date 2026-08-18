# Outillage de session — rapatrié le 18/08/2026 pour la passation

Ces scripts vivaient dans `~/.radar-session/` sur le Mac de Gérald et faisaient
tourner les grandes campagnes (séjours, invitations, traductions). Ils sont ici
pour que la personne qui reprend le site hérite de TOUT, pas seulement du site.

- `publier.sh` — l'unique porte de sortie : récolte (inject.py), reconstruit,
  VALIDE (validate.py refuse de pousser au moindre blocage), commit, push.
- `reste.py` — les trois compteurs d'avancement (traductions, séjours, invitations).
- `inject.py` — récolte les résultats des ateliers d'agents dans les données.
- `preparer_recherche.py` / `preparer_verif.py` — fabriquent les ateliers
  (composition puis contrôle adverse) à partir des gabarits de `gabarits/`.
- `hb.sh` — la sonde de battement pendant qu'une flotte tourne.

ATTENTION, à adapter sur une nouvelle machine : ces scripts contiennent des
chemins absolus propres au Mac et à la session Claude Code d'origine (le dossier
des journaux d'ateliers, `~/luxe-ete-2026`). Demander à Claude de les adapter
est l'affaire de cinq minutes : les chemins sont en tête de chaque fichier.

La doctrine et les leçons durables, elles, sont déjà dans le dépôt :
`.radar/DOCTRINE.md`, `.radar/tools/lessons.md`, les registres `.radar/*.json`.
