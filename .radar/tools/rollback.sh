#!/usr/bin/env bash
# rollback.sh — retour arrière SÛR si une régression est détectée en ligne.
#
# À déclencher si, APRÈS publication, healthcheck.sh ou perfcheck.py signale une
# régression (contenu perdu, poids gonflé, site figé/KO). Annule le dernier commit
# via `git revert` (crée un commit d'annulation — PAS de réécriture d'historique,
# pas de force-push), repousse, et revérifie. C'est le filet qui garantit que
# même une erreur en autonomie ne laisse jamais les internautes sur une version
# dégradée.
#
# Usage : bash rollback.sh ["raison courte"]
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${RADAR_REPO:-/Users/geraldlefebvre/luxe-ete-2026}"
GH="$(command -v gh || echo /Users/geraldlefebvre/bin/gh)"
REASON="${1:-régression détectée par le filet}"

cd "$REPO" || { echo "rollback: dépôt introuvable ($REPO)"; exit 2; }

if [ -n "$(git status --porcelain)" ]; then
  echo "rollback: ⚠️ modifications non commitées présentes — les traiter d'abord (rien annulé)."
  git --no-pager status --short
  exit 2
fi

LAST="$(git log --oneline -1)"
echo "rollback: annulation du dernier commit → $LAST"
echo "rollback: raison : $REASON"

if ! git revert --no-edit HEAD; then
  echo "rollback: ❌ git revert a échoué (conflit ?) — intervention manuelle requise."
  git revert --abort 2>/dev/null || true
  exit 1
fi

if ! git push origin HEAD; then
  echo "rollback: ❌ push du revert échoué — le revert est local, à pousser manuellement."
  exit 1
fi

echo "rollback: revert poussé. Revérification via healthcheck…"
sleep 5
bash "$DIR/healthcheck.sh"
