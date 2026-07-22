#!/usr/bin/env bash
# precheck.sh — à lancer en TOUT DÉBUT de passe (avant toute recherche/édition).
#
# Détecte un run précédent interrompu : index.html modifié mais NON COMMITÉ dans
# le dépôt public. C'est exactement l'état trouvé le 17/07/2026 (un run stoppé
# après 66 traductions mais avant le commit). Le script se contente de SIGNALER
# et de lancer validate.py — il ne commite ni ne jette rien : l'opérateur décide
# (conserver le travail s'il est bon, sinon `git checkout -- index.html`).
# NE TOUCHE JAMAIS le fichier public.
#
# Usage : bash precheck.sh [chemin/dépôt]   (défaut : ~/luxe-ete-2026)
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${1:-${RADAR_REPO:-/Users/geraldlefebvre/luxe-ete-2026}}"

if [ ! -d "$REPO/.git" ]; then
  echo "precheck: dépôt git introuvable ($REPO)"
  exit 2
fi

# --- Verrou de passe (anti-concurrence) ---
# Le 17/07/2026, DEUX passes ont tourné en parallèle sur le même dépôt (risque de
# conflit / publication écrasée). Le verrou empêche une 2e passe de démarrer si
# une autre est en cours. Auto-expiration à 4 h : le 22/07/2026 une passe complète
# a duré plus de 90 min (grosses vagues de traduction), le verrou a expiré en cours
# de route et une 2e passe a commité par-dessus. À lever en fin de passe :
# rm -f "$DIR/.lock".
LOCK="$DIR/.lock"
if [ -f "$LOCK" ]; then
  LOCK_TS="$(tr -dc '0-9' < "$LOCK" 2>/dev/null || echo 0)"
  NOW="$(date +%s)"
  AGE=$(( NOW - ${LOCK_TS:-0} ))
  if [ "$AGE" -ge 0 ] && [ "$AGE" -lt 14400 ]; then
    echo "precheck: 🔒 STOP — une autre passe semble EN COURS (verrou posé il y a ${AGE}s)."
    echo "          Ne pas démarrer une passe concurrente. Si c'est un verrou orphelin,"
    echo "          le supprimer : rm -f \"$LOCK\"."
    exit 3
  fi
  echo "precheck: verrou périmé (${AGE}s) ignoré — reprise."
fi
date +%s > "$LOCK"

# --- Contrôle de CADENCE (leçon du 21/07/2026) ---
# Le cron s'est tu du 18 au 20/07 (4 jours sans passe) et RIEN ne le signalait.
# La cadence nominale est 2 passes/jour : si le dernier run journalisé
# (tools/run-log.ndjson, écrit par healthcheck) date de plus de 14 h, on doit
# le dire haut et fort — et le compte rendu à Gérald doit le mentionner.
RUNLOG="$DIR/run-log.ndjson"
if [ -f "$RUNLOG" ]; then
  LAST_TS="$(tail -1 "$RUNLOG" | sed -n 's/.*"ts":"\([^"]*\)".*/\1/p')"
  if [ -n "$LAST_TS" ]; then
    # `date -j -f` est propre à BSD/macOS. Sous Linux (exécution cloud) il échoue,
    # et l'ancien « || echo 0 » DÉSACTIVAIT alors le contrôle de cadence en
    # silence — exactement le défaut qu'il était censé corriger. Repli GNU puis
    # python3 (toujours présent, les outils du filet en dépendent déjà).
    LAST_EPOCH="$(date -j -u -f '%Y-%m-%dT%H:%M:%SZ' "$LAST_TS" +%s 2>/dev/null \
      || date -u -d "$LAST_TS" +%s 2>/dev/null \
      || python3 -c "import datetime,sys;print(int(datetime.datetime.strptime(sys.argv[1],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc).timestamp()))" "$LAST_TS" 2>/dev/null \
      || echo 0)"
    if [ "$LAST_EPOCH" -eq 0 ]; then
      echo "precheck: ⚠️  horodatage du dernier run illisible ($LAST_TS) — contrôle de cadence INOPÉRANT, à signaler."
    fi
    if [ "$LAST_EPOCH" -gt 0 ]; then
      GAP=$(( $(date +%s) - LAST_EPOCH ))
      if [ "$GAP" -gt 50400 ]; then
        echo "precheck: ⏰ CADENCE ROMPUE — dernier run journalisé il y a $(( GAP / 3600 )) h (> 14 h)."
        echo "          Des passes ont été manquées : faire une passe de RATTRAPAGE (complète)"
        echo "          et SIGNALER l'anomalie de déclenchement dans le compte rendu."
      fi
    fi
  fi
fi
echo "precheck: 🔓 verrou de passe posé ($LOCK) — à lever en fin de passe (rm -f)."

DIRTY="$(git -C "$REPO" status --porcelain -- index.html 2>/dev/null)"
if [ -n "$DIRTY" ]; then
  echo "precheck: ⚠️  index.html présente des modifications NON COMMITÉES"
  echo "          (probable run précédent interrompu AVANT le commit)."
  echo "          → Diagnostiquer AVANT de démarrer : conserver si le travail est bon,"
  echo "            sinon 'git -C \"$REPO\" checkout -- index.html'."
  git -C "$REPO" --no-pager diff --stat -- index.html
else
  echo "precheck: arbre propre — index.html sans modification non commitée."
fi

# État de synchro avec le distant (une passe concurrente peut avoir poussé).
git -C "$REPO" fetch --quiet origin 2>/dev/null || true
LOCAL="$(git -C "$REPO" rev-parse HEAD 2>/dev/null || echo '?')"
REMOTE="$(git -C "$REPO" rev-parse '@{u}' 2>/dev/null || echo '?')"
if [ "$LOCAL" != "$REMOTE" ] && [ "$REMOTE" != "?" ]; then
  echo "precheck: ⚠️  HEAD local ($LOCAL) ≠ distant ($REMOTE) — une autre passe a peut-être publié."
  echo "          → 'git -C \"$REPO\" pull --rebase' avant de démarrer, pour ne pas écraser son travail."
fi

echo "precheck: lancement de validate.py sur l'état courant…"
python3 "$DIR/validate.py" "$REPO/index.html"
