#!/bin/zsh
# Passation du 18/08/2026 : le chemin des ateliers était celui d'UNE session
# Claude Code sur le Mac de Gérald. On le retrouve maintenant par le nom de
# l'atelier, dans n'importe quelle session de la machine courante.
RACINE="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
now=$(date +%s); line="💓 $(date +%H:%M:%S)"
for e in "${(@f)$(cat $HOME/.radar-session/ateliers 2>/dev/null)}"; do
  [ -z "$e" ] && continue
  id="${e%% *}"; nom="${e#* }"; nom="${nom%% *}"; cible="${e##* }"
  D=$(ls -d "$RACINE"/projects/*/*/subagents/workflows/"$id" 2>/dev/null | head -1)
  [ -z "$D" ] && { line="$line · $nom introuvable"; continue; }
  n=$(grep -c '"type":"result"' "$D/journal.jsonl" 2>/dev/null|head -1); n=${n:-0}
  last=$(ls -t "$D"/*.jsonl 2>/dev/null|head -1)
  age=$(( now - $(stat -f %m "$last" 2>/dev/null || echo $now) ))
  mark=""; [ $age -gt 300 ] && [ "$n" -lt "$cible" ] && mark=" ⚠️MORT(${age}s)"
  line="$line · $nom $n/$cible$mark"
done
echo "$line"
