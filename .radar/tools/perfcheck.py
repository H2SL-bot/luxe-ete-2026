#!/usr/bin/env python3
"""perfcheck.py — garde-fou de PERFORMANCE et de NON-RÉGRESSION du radar.

Rôle : rendre sûres les optimisations de vitesse faites en autonomie. Il mesure
le poids réellement transféré (gzip) et l'inventaire de CONTENU (nombre d'événe-
ments, langues présentes), les journalise dans perf-log.ndjson, et ÉCHOUE
(code != 0) si un changement a fait RÉGRESSER le contenu ou gonflé le poids sans
raison. C'est la barrière qui garantit « jamais d'impact négatif pour l'inter-
naute » : on ne publie une optimisation que si perfcheck reste vert.

Contrôles RÉGRESSION (BLOCKER) vs le dernier point de perf-log :
  - perte de contenu : moins d'événements qu'avant ;
  - langue disparue : une langue présente avant ne l'est plus ;
  - bloat : poids gzip > +20 % sans hausse du nombre d'événements.

Le prix de l'optimisation « une seule langue au 1er chargement » (poids FR seul
vs poids complet) est calculé et suivi à chaque passe, pour piloter le gain.

Usage : python3 perfcheck.py [chemin/index.html]   (défaut : ~/luxe-ete-2026)
        python3 perfcheck.py --baseline   (enregistre sans comparer, 1re fois)
"""
import re, os, sys, json, gzip, io
from datetime import date

DEFAULT = os.environ.get("RADAR_REPO", "/Users/geraldlefebvre/luxe-ete-2026") + "/index.html"
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "perf-log.ndjson")
LANGS = ["en", "es", "it", "pt", "de", "ru", "ar", "zh", "ja", "ko"]


def gz(obj):
    b = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return len(b), len(gzip.compress(b, 9))


def measure(path):
    html = open(path, encoding="utf-8").read()
    m = re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S)
    evts = json.loads(m.group(1).replace("<\\/", "</"))
    page_gzip = len(gzip.compress(html.encode("utf-8"), 9))
    # Traductions différées : quand i18n-data/ existe, l'inventaire de contenu
    # (nb de langues) doit continuer à les compter — sinon la garde de
    # non-régression croirait à une disparition de langues. Le POIDS mesuré,
    # lui, reste celui de la page seule : c'est bien ce que l'internaute
    # télécharge au premier affichage.
    i18n_dir = os.path.join(os.path.dirname(os.path.abspath(path)), "i18n-data")
    if os.path.isdir(i18n_dir):
        for fn in sorted(os.listdir(i18n_dir)):
            if not fn.endswith(".json"):
                continue
            try:
                arr = json.load(open(os.path.join(i18n_dir, fn), encoding="utf-8"))
            except Exception:
                continue
            if isinstance(arr, dict):
                keys = {f"{e.get('d1','')}|{e.get('n','')}": e for e in evts}
                for k, t in arr.items():
                    e = keys.get(k)
                    if e is not None and t:
                        e.setdefault("tr", {})[fn[:-5]] = t
    _, data_gzip = gz(evts)
    fr_only = [{k: v for k, v in e.items() if k != "tr"} for e in evts]
    _, fr_gzip = gz(fr_only)
    langs = set()
    for e in evts:
        langs |= set((e.get("tr") or {}).keys())
    return {
        "events": len(evts),
        "langs": sorted(langs),
        "page_gzip": page_gzip,
        "data_gzip": data_gzip,
        "fr_only_gzip": fr_gzip,  # payload initial visé si langues différées
    }


def last_record():
    if not os.path.exists(LOG):
        return None
    rec = None
    for line in open(LOG, encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                rec = json.loads(line)
            except Exception:
                pass
    return rec


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    baseline_only = "--baseline" in sys.argv
    path = args[0] if args else DEFAULT
    cur = measure(path)
    prev = last_record()

    blockers = []
    if prev and not baseline_only:
        if cur["events"] < prev.get("events", 0):
            blockers.append(f"perte de contenu : {prev['events']} -> {cur['events']} événements")
        lost = set(prev.get("langs", [])) - set(cur["langs"])
        if lost:
            blockers.append(f"langue(s) disparue(s) : {', '.join(sorted(lost))}")
        pg, pp = cur["page_gzip"], prev.get("page_gzip", 0)
        if pp and cur["events"] <= prev.get("events", 0) and pg > pp * 1.20:
            blockers.append(f"bloat : poids gzip {pp/1e6:.2f} -> {pg/1e6:.2f} Mo (>+20%) sans contenu en plus")

    mb = lambda x: f"{x/1e6:.2f} Mo"
    print(f"=== perfcheck.py — {path} ===")
    print(f"événements            : {cur['events']}")
    print(f"langues (tr)          : {len(cur['langs'])} ({','.join(cur['langs'])})")
    print(f"poids page (gzip)     : {mb(cur['page_gzip'])}   <- transfert internaute (approx.)")
    print(f"  dont bloc data      : {mb(cur['data_gzip'])}")
    print(f"payload FR seul (gzip): {mb(cur['fr_only_gzip'])}   <- cible si 10 langues différées")
    if cur["data_gzip"]:
        save = cur["data_gzip"] - cur["fr_only_gzip"]
        print(f"gain potentiel diff.  : -{mb(save)} sur le data  (~-{100*save//cur['data_gzip']}%, "
              f"~{cur['data_gzip']/max(cur['fr_only_gzip'],1):.1f}x plus léger)")
    if prev:
        d = cur["page_gzip"] - prev.get("page_gzip", 0)
        print(f"vs dernier point      : {'+' if d>=0 else ''}{d/1e6:.2f} Mo poids, "
              f"{cur['events']-prev.get('events',0):+d} événements")

    for b in blockers:
        print("REGRESSION ", b)

    if not blockers:
        rec = dict(cur)
        rec["date"] = date.today().isoformat()
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"\n{'FAIL (régression)' if blockers else 'OK'} — {len(blockers)} régression(s)")
    sys.exit(1 if blockers else 0)


if __name__ == "__main__":
    main()
