#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_full.py — reconstruit index-full.html à partir des fichiers VERSIONNÉS.

Pourquoi : index-full.html (10,7 Mo) réécrit à chaque passe faisait grossir le
dépôt de plusieurs gigaoctets par an et alourdissait chaque clonage — y compris
celui des sessions cloud, soupçonné de les étouffer. Il n'est PLUS versionné.

Il est pourtant strictement redondant : index.html (léger, français seul) +
i18n-data/<lang>.json (une langue par fichier, clé stable « d1|nom »)
contiennent exactement la même information. Ce script refait la somme :

    index-full.html = index.html + toutes les traductions réinjectées dans `tr`

À lancer AU DÉBUT de toute passe (routine cloud, plancher, session locale) si
index-full.html est absent. split_i18n.py refait ensuite le chemin inverse.
"""
import argparse
import glob
import json
import os
import re
import sys

REPO = os.environ.get("RADAR_REPO", "/Users/geraldlefebvre/luxe-ete-2026")
LIGHT = os.path.join(REPO, "index.html")
I18N_DIR = os.path.join(REPO, "i18n-data")
DATA_RE = re.compile(r'(<script type="application/json" id="data">)(.*?)(</script>)', re.S)


def key_of(e):
    return f"{e.get('d1', '')}|{e.get('n', '')}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(REPO, "index-full.html"))
    a = ap.parse_args()

    if not os.path.exists(LIGHT):
        sys.exit("rebuild_full: index.html introuvable")
    if not os.path.isdir(I18N_DIR):
        sys.exit("rebuild_full: i18n-data/ introuvable")

    html = open(LIGHT, encoding="utf-8").read()
    m = DATA_RE.search(html)
    if not m:
        sys.exit("rebuild_full: bloc data introuvable dans index.html")
    data = json.loads(m.group(2).replace("<\\/", "</"))
    index = {key_of(e): e for e in data}

    langs, orphelins, injectes = [], 0, 0
    for p in sorted(glob.glob(os.path.join(I18N_DIR, "*.json"))):
        lang = os.path.splitext(os.path.basename(p))[0]
        langs.append(lang)
        table = json.load(open(p, encoding="utf-8"))
        for k, t in table.items():
            e = index.get(k)
            if e is None:
                orphelins += 1
                continue
            e.setdefault("tr", {})[lang] = t
            injectes += 1

    neuf = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    full = html[:m.start(2)] + neuf + html[m.end(2):]

    if len(full) <= len(html):
        sys.exit("rebuild_full: le résultat n'est pas plus lourd que l'index léger — "
                 "les traductions n'ont pas été injectées, on n'écrit rien.")

    open(a.out, "w", encoding="utf-8").write(full)
    avec_tr = sum(1 for e in data if e.get("tr"))
    print("=== rebuild_full ===")
    print(f"événements            : {len(data)}  (avec traductions : {avec_tr})")
    print(f"langues réinjectées   : {len(langs)}  ({','.join(langs)})")
    print(f"entrées injectées     : {injectes}  | orphelines (clé sans fiche) : {orphelins}")
    print(f"écrit                 : {a.out}  ({os.path.getsize(a.out) / 1e6:.2f} Mo)")
    if orphelins:
        print("NOTE : des orphelines existent — normal juste après une purge ; "
              "split_i18n.py les fera disparaître à la prochaine régénération.")


if __name__ == "__main__":
    main()
