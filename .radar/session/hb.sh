#!/bin/zsh
W="/Users/geraldlefebvre/.claude/projects/-Users-geraldlefebvre/2de0cd85-85f8-41f3-aca5-7906e9758743/subagents/workflows"
now=$(date +%s); line="💓 $(date +%H:%M:%S)"
for e in "${(@f)$(cat $HOME/.radar-session/ateliers 2>/dev/null)}"; do
  [ -z "$e" ] && continue
  id="${e%% *}"; nom="${e#* }"; nom="${nom%% *}"; cible="${e##* }"
  n=$(grep -c '"type":"result"' "$W/$id/journal.jsonl" 2>/dev/null|head -1); n=${n:-0}
  last=$(ls -t "$W/$id"/*.jsonl 2>/dev/null|head -1)
  age=$(( now - $(stat -f %m "$last" 2>/dev/null || echo $now) ))
  mark=""; [ $age -gt 300 ] && [ "$n" -lt "$cible" ] && mark=" ⚠️MORT(${age}s)"
  line="$line · $nom $n/$cible$mark"
done
echo "$line"
