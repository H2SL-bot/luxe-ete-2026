#!/bin/zsh
# Publieur au fil de l'eau. NE PUBLIE JAMAIS si validate.py échoue.
set -e

# Passation du 18/08/2026 : ce script portait le chemin du Mac de Gérald en dur,
# plus un renvoi vers ~/.radar-session/ qui n'existe que chez lui. Sur toute
# autre machine il s'arrêtait à la deuxième ligne — la « porte de sortie
# unique » était donc condamnée. On déduit désormais le dépôt de l'emplacement
# du script lui-même : il fonctionne partout, sans réglage.
# Écriture volontairement portable : la passation documente « bash publier.sh »
# alors que l'en-tête dit zsh. Les modificateurs zsh (${0:A:h}) cassent sous
# bash — ce qui a été découvert au premier essai réel. Ceci marche sous les deux.
_ICI=$(cd "$(dirname "$0")" && pwd)
REPO="${RADAR_REPO:-$(cd "$_ICI/../.." && pwd)}"
cd "$REPO"
export RADAR_REPO="$PWD"
[ -f "$PWD/index.html" ] || { echo "⛔ $PWD ne contient pas index.html — refus d'agir"; exit 1; }
# L'apostrophe de « l'eau » à l'intérieur de ${1:-...} faisait échouer bash à
# l'analyse : le script n'a jamais été exécutable par la commande que PASSATION.md
# documente (« bash .radar/session/publier.sh »). Valeur par défaut sortie de
# l'expansion : lisible, et valide sous les deux interpréteurs.
MSG="$1"
[ -n "$MSG" ] || MSG="Publication au fil de l'eau"

# index-full.html (15 Mo) n'est pas versionné : il alourdissait chaque clonage.
# Tous les outils ci-dessous le lisent. La passe automatique le reconstruit déjà
# quand il manque ; le publieur ne le faisait pas et échouait donc sur une
# machine fraîchement clonée. Même réflexe ici.
[ -f index-full.html ] || python3 .radar/tools/rebuild_full.py >/dev/null

# inject.py est rapatrié DANS le dépôt (.radar/session/) et ne vit plus dans
# ~/.radar-session/. Il récolte les ateliers d'agents : s'il n'y en a aucun sur
# cette machine, il n'a rien à faire et ne doit pas bloquer la publication.
python3 .radar/session/inject.py || echo "· inject : rien à récolter, on continue"
python3 .radar/tools/split_i18n.py --apply >/dev/null
# gen_seo.py — étape 7bis de la doctrine, absente du publieur depuis toujours :
# elle ne tournait que dans la passe du matin. Depuis l'arrêt de cette passe
# le 18/08/2026, le socle SEO (statut de l'événement, organisateur, accès
# gratuit ou payant, tarifs réels dans le ld+json) n'était plus rafraîchi.
# Ordre imposé par la doctrine : split_i18n → gen_seo → gen_pages.
python3 .radar/tools/gen_seo.py >/dev/null
python3 .radar/tools/gen_pages.py >/dev/null
V=$(python3 .radar/tools/validate.py 2>&1 | tail -1)
echo "$V"
case "$V" in
  OK*) ;;
  *) echo "⛔ PUBLICATION REFUSÉE — validate.py en échec, rien n'est parti en ligne"; exit 1;;
esac
if [ -z "$(git status --porcelain)" ]; then echo "· rien de neuf"; exit 0; fi
git add -A
git commit -q -m "$MSG

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01JRyTnDUWpbLSg2Hef7kFRs"
if git push -q origin main 2>/dev/null; then echo "POUSSÉ"; else
  echo "⚠️ push refusé — la routine a publié en parallèle, remise à plat"
  git reset --hard -q HEAD~1
  git fetch -q origin main && git reset --hard -q origin/main
  python3 .radar/tools/rebuild_full.py >/dev/null
  echo "· base réalignée sur la vérité publiée ; relancez"
  exit 2
fi
