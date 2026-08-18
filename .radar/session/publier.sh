#!/bin/zsh
# Publieur au fil de l'eau. NE PUBLIE JAMAIS si validate.py échoue.
set -e
cd /Users/geraldlefebvre/luxe-ete-2026
export RADAR_REPO="$PWD"
MSG="${1:-Publication au fil de l'eau}"
python3 $HOME/.radar-session/inject.py
python3 .radar/tools/split_i18n.py --apply >/dev/null
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

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
if git push -q origin main 2>/dev/null; then echo "POUSSÉ"; else
  echo "⚠️ push refusé — la routine a publié en parallèle, remise à plat"
  git reset --hard -q HEAD~1
  git fetch -q origin main && git reset --hard -q origin/main
  python3 .radar/tools/rebuild_full.py >/dev/null
  echo "· base réalignée sur la vérité publiée ; relancez"
  exit 2
fi
