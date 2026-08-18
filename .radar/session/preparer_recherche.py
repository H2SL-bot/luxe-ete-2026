"""Écrit un atelier de RECHERCHE pour les fiches auxquelles il manque un séjour ou
une voie d'invitation.

    usage : preparer_recherche.py <sej|inv> <nom_atelier> [taille] [décalage]

Priorité : les fiches À VENIR OU EN COURS d'abord, les plus proches en tête — ce sont
celles que le visiteur a sous les yeux. Les fiches déjà passées (gardées trente jours)
viennent après, car les enrichir ne sert plus personne.

Les fiches déjà confiées à un chercheur ou à un contrôleur encore actif sont exclues,
pour ne pas payer deux fois le même travail (fichier ~/.radar-session/ateliers-encours).
"""
import datetime as dt
import json
import os
import re
import sys

REPO = "/Users/geraldlefebvre/luxe-ete-2026"
S = "/private/tmp/claude-501/-Users-geraldlefebvre/2de0cd85-85f8-41f3-aca5-7906e9758743/scratchpad"
ENCOURS = os.path.expanduser("~/.radar-session/ateliers-encours")

kind = sys.argv[1]
nom = sys.argv[2]
taille = int(sys.argv[3]) if len(sys.argv) > 3 else 12
decalage = int(sys.argv[4]) if len(sys.argv) > 4 else 0
champ = "sej" if kind == "sej" else "iv"

doc = open(os.path.join(REPO, "index-full.html"), encoding="utf-8").read()
data = json.loads(re.search(r'id="data">(.*?)</script>', doc, re.S).group(1).replace("<\\/", "</"))


def parse(s):
    try:
        return dt.date.fromisoformat((s or "")[:10])
    except Exception:
        return None


deja = set()
if os.path.exists(ENCOURS):
    deja = {l.strip() for l in open(ENCOURS, encoding="utf-8") if l.strip()}

aujourdhui = dt.date.today()
manquants = []
for e in data:
    if e.get(champ):
        continue
    n = e.get("n") or ""
    if not n or n in deja:
        continue
    fin = parse(e.get("d2")) or parse(e.get("d1"))
    debut = parse(e.get("d1")) or fin
    # passé = terminé ; on le traite en dernier
    passe = 1 if (fin and fin < aujourdhui) else 0
    manquants.append((passe, debut or dt.date(2099, 1, 1), e))

manquants.sort(key=lambda t: (t[0], t[1]))
lot = manquants[decalage:decalage + taille]

cibles = [{"cle": f"{e.get('d1','')}|{e.get('n','')}", "nom": e.get("n", ""),
           "ville": e.get("v", ""), "lieu": (e.get("l") or "")[:150],
           "d1": e.get("d1", ""), "d2": e.get("d2", "")}
          for _, _, e in lot]

# Les gabarits vivaient dans le scratchpad, effacé à chaque redémarrage : le
# 18/08/2026 la chaîne entière est tombée pour cette seule raison. Ils vivent
# désormais dans ~/.radar-session/gabarits/, qui survit.
G = os.path.expanduser("~/.radar-session/gabarits")
tete = open(f"{G}/tpl-{kind}-tete.txt", encoding="utf-8").read()
corps = open(f"{G}/tpl-{kind}-corps.txt", encoding="utf-8").read()
tete = re.sub(r"name: '[^']*'", f"name: '{nom}'", tete, count=1)
tete = re.sub(r"description: '[^']*'",
              f"description: 'Composer {len(cibles)} fiches lot {nom}'", tete, count=1)

script = tete + "const A=JSON.parse(" + json.dumps(json.dumps(cibles, ensure_ascii=False)) + ");\n" + corps
open(f"{S}/{nom}.js", "w", encoding="utf-8").write(script)

with open(ENCOURS, "a", encoding="utf-8") as fh:
    for c in cibles:
        fh.write(c["nom"] + "\n")

restants = len(manquants) - decalage - len(cibles)
avenir = sum(1 for p, _, _ in manquants if p == 0)
print(f"{nom} : {len(cibles)} fiches → {S}/{nom}.js")
print(f"   manquants {champ} : {len(manquants)} (dont {avenir} à venir/en cours) — reste après ce lot : {max(0, restants)}")
for c in cibles[:3]:
    print(f"   · {c['nom'][:62]}")
