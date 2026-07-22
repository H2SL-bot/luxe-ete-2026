#!/usr/bin/env bash
# healthcheck.sh — sonde post-publication du radar ConstanceParis7.
#
# À lancer APRÈS le push / la republication (fin de PROCÉDURE). Vérifie que le
# site public répond 200, montre la date du jour (eyebrow du masthead) ET sert
# bien le NOUVEAU build — via un marqueur de version : le compte d'événements
# servi doit égaler le dernier build validé (tools/.last-count, écrit par
# validate.py). Journalise chaque exécution dans run-log.ndjson (append-only).
# Sort en code != 0 si le site est KO, périmé, ou fige une ANCIENNE version.
#
# Robustesse : boucle de propagation (le CDN GitHub Pages met ~15 s à qq min à
# servir le nouveau build) — sur le chemin heureux (déjà en ligne) une seule
# itération. Rétro-compatible : si python3 ou .last-count manquent, on retombe
# sur le seul contrôle de date (comportement d'origine). NE MODIFIE JAMAIS le
# fichier public : le marqueur de version vit uniquement côté outils.
#
# Usage : bash healthcheck.sh [URL]   (défaut : https://constanceparis7.com/)
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$DIR/run-log.ndjson"
STATE="$DIR/.last-count"
URL="${1:-https://constanceparis7.com/}"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Date française attendue dans l'eyebrow, ex. "16 juillet 2026".
# BSD date (macOS) ne gère pas %-d de façon fiable -> on retire le zéro à la main.
# Tolérance de fraîcheur : AUJOURD'HUI ou HIER (entre minuit et la passe du matin
# le site montre légitimement la veille). 2 jours ou plus = vraie passe manquée.
MONTHS=(x janvier février mars avril mai juin juillet août septembre octobre novembre décembre)
# `date -v` est propre à BSD/macOS ; l'exécution cloud tourne sous Linux, où il
# faut `date -d`. Sans ce repli, la sonde de fraîcheur échouait en silence dès la
# première passe distante (leçon du 22/07/2026, avant la migration).
day_of() {  # $1 = décalage jours, $2 = format strftime
  date -v-"$1"d "+$2" 2>/dev/null \
    || date -d "-$1 days" "+$2" 2>/dev/null \
    || python3 -c "import datetime,sys;print((datetime.date.today()-datetime.timedelta(days=int(sys.argv[1]))).strftime(sys.argv[2]))" "$1" "$2" 2>/dev/null
}
fr_date() {  # $1 = décalage jours (0 = aujourd'hui, 1 = hier)
  local d m y
  d="$(day_of "$1" %d | sed 's/^0//')"
  m="$(day_of "$1" %m | sed 's/^0//')"
  y="$(day_of "$1" %Y)"
  echo "${d} ${MONTHS[$m]} ${y}"
}
EXPECTED="$(fr_date 0)"
EXPECTED_Y="$(fr_date 1)"

# Compte d'événements attendu = dernier build validé (marqueur de version local).
EXP_COUNT=""
[ -f "$STATE" ] && EXP_COUNT="$(tr -dc '0-9' < "$STATE")"

TMP="$(mktemp -t ccp7health.XXXXXX)"
trap 'rm -f "$TMP"' EXIT

fetch() {  # un seul appel : corps -> $TMP, code HTTP -> stdout
  curl -s -A "$UA" --max-time 25 -L "$URL" -o "$TMP" -w '%{http_code}' 2>/dev/null || echo "000"
}
date_ok() { grep -qF "$EXPECTED" "$TMP" 2>/dev/null || grep -qF "$EXPECTED_Y" "$TMP" 2>/dev/null; }
live_count() {  # compte les événements du bloc data servi ; "" si indisponible
  python3 - "$TMP" <<'PY' 2>/dev/null || echo ""
import sys, re, json
try:
    s = open(sys.argv[1], encoding="utf-8").read()
    m = re.search(r'<script type="application/json" id="data">(.*?)</script>', s, re.S)
    print(len(json.loads(m.group(1).replace('<\\/', '</'))) if m else "")
except Exception:
    print("")
PY
}

# Boucle de propagation : on attend que le build ATTENDU soit servi (date fraîche
# + compte == attendu). Une seule itération si déjà en ligne.
ATTEMPTS=10
SLEEP=15
CODE="000"; HAS_DATE="no"; LC=""; MATCH="no"
for i in $(seq 1 "$ATTEMPTS"); do
  CODE="$(fetch)"
  HAS_DATE="no"; date_ok && HAS_DATE="yes"
  LC="$(live_count)"
  if [ "$CODE" = "200" ] && [ "$HAS_DATE" = "yes" ]; then
    # Version OK si compte connu == attendu. Si le compte de référence manque
    # (état perdu, python indisponible), on ne peut PAS conclure : on retombe sur
    # le seul contrôle de date, mais on le DIT — un contrôle qui se désactive en
    # silence est pire que pas de contrôle du tout.
    if [ -z "$EXP_COUNT" ] || [ -z "$LC" ]; then
      echo "healthcheck: ⚠️  contrôle de VERSION impossible (attendu='${EXP_COUNT:-?}', servi='${LC:-?}') — seule la date est vérifiée."
      MATCH="degrade"; break
    fi
    if [ "$LC" = "$EXP_COUNT" ]; then MATCH="yes"; break; fi
  fi
  [ "$i" -lt "$ATTEMPTS" ] && sleep "$SLEEP"
done

# « degrade » = site vivant et daté du jour, mais version non vérifiable : ce
# n'est pas une alerte (le site va bien), c'est un contrôle en moins. On sort en
# succès tout en le consignant, pour ne pas déclencher un rollback pour rien.
OK="no"
case "$MATCH" in yes) OK="yes" ;; degrade) OK="degrade" ;; esac

printf '{"ts":"%s","url":"%s","http":"%s","date_present":"%s","live_count":"%s","expected_count":"%s","expected_date":"%s (ou %s)","ok":"%s"}\n' \
  "$TS" "$URL" "$CODE" "$HAS_DATE" "${LC:-?}" "${EXP_COUNT:-?}" "$EXPECTED" "$EXPECTED_Y" "$OK" >> "$LOG"

echo "healthcheck: http=$CODE  date_fraiche=$HAS_DATE  compte_live=${LC:-?}  attendu=${EXP_COUNT:-?}  ->  $OK"
if [ "$OK" = "degrade" ]; then
  echo "healthcheck: site en ligne et daté du jour, mais version non vérifiée — à signaler au compte rendu."
  exit 0
fi
if [ "$OK" != "yes" ]; then
  if [ "$CODE" = "200" ] && [ -n "$EXP_COUNT" ] && [ -n "$LC" ] && [ "$LC" != "$EXP_COUNT" ]; then
    echo "ALERTE: le live sert $LC événements, attendu $EXP_COUNT — nouveau build non propagé ou publication ratée ?"
  else
    echo "ALERTE: le site public est KO ou ne montre pas la date du jour — passe manquée ou publication ratée ?"
  fi
  exit 1
fi
exit 0
