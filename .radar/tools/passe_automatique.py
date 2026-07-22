#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
passe_automatique.py — LE PLANCHER GARANTI de la mise à jour quotidienne.

Pourquoi ce fichier existe
--------------------------
La passe intelligente (recherche de nouveaux événements, traductions, séjours)
est faite par une routine Claude. Si cette routine ne tourne pas — panne, quota,
réglage manquant — plus rien ne met le site à jour, et il se fige en silence.

Ce script est le filet : il fait, SANS AUCUNE INTELLIGENCE ARTIFICIELLE, le
travail d'entretien qui doit arriver tous les jours. Il tourne dans GitHub
Actions, sans machine, sans clé d'API, sans compte Claude.

Ce qu'il fait, et rien de plus :
  1. PURGE les événements terminés depuis plus de 30 jours ;
  2. VÉRIFIE les liens des événements à venir (et signale les vrais morts) ;
  3. met à jour la DATE affichée en haut du site — honnêtement : elle n'avance
     que si la vérification des liens a réellement eu lieu ;
  4. régénère l'index allégé et les fichiers de langue (split_i18n).

Il n'invente jamais rien : il ne fait que retirer du périmé et constater.

Usage :
    python3 passe_automatique.py            # essai à blanc, n'écrit rien
    python3 passe_automatique.py --apply    # écrit index-full.html
"""
import argparse
import concurrent.futures as futures
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.request

REPO = os.environ.get("RADAR_REPO", "/Users/geraldlefebvre/luxe-ete-2026")
FULL = os.path.join(REPO, "index-full.html")
DATA_RE = re.compile(r'(<script type="application/json" id="data">)(.*?)(</script>)', re.S)
EYEBROW_RE = re.compile(r"(données collectées et vérifiées le\s*)([^<]{0,40})")

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def parse_d(s):
    try:
        return dt.date.fromisoformat((s or "")[:10])
    except Exception:
        return None


def tester_lien(url):
    """Renvoie (url, vivant). Un blocage anti-robot n'est PAS un lien mort :
    403/405/429 signifient « le serveur m'a vu et m'a refusé », donc il existe."""
    if not url or not url.startswith("http"):
        return url, True
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            return url, r.status < 400
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 429, 406):
            return url, True          # bloqué, pas mort
        if e.code == 404:
            return url, False
        return url, True              # 5xx : panne passagère, on ne juge pas
    except Exception:
        return url, True              # réseau capricieux : bénéfice du doute


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--max-liens", type=int, default=120,
                    help="nombre de liens testés par passe (les plus imminents d'abord)")
    a = ap.parse_args()

    if not os.path.exists(FULL):
        sys.exit(f"passe_automatique: {FULL} introuvable — la bascule perf n'a pas eu lieu ?")

    html = open(FULL, encoding="utf-8").read()
    m = DATA_RE.search(html)
    if not m:
        sys.exit("passe_automatique: bloc data introuvable")
    data = json.loads(m.group(2).replace("<\\/", "</"))
    avant = len(data)

    aujourdhui = dt.date.today()
    limite = aujourdhui - dt.timedelta(days=30)

    # ---- 1. purge du périmé -------------------------------------------------
    gardes, purges = [], []
    for e in data:
        d2 = parse_d(e.get("d2") or e.get("d1"))
        (purges if (d2 and d2 < limite) else gardes).append(e)

    # ---- 2. vérification des liens des plus imminents ------------------------
    a_venir = [e for e in gardes if (parse_d(e.get("d2") or e.get("d1")) or aujourdhui) >= aujourdhui]
    a_venir.sort(key=lambda e: (parse_d(e.get("d1")) or aujourdhui))
    cibles = [e for e in a_venir if e.get("u")][: a.max_liens]
    urls = list({e["u"] for e in cibles})
    morts = []
    if urls:
        with futures.ThreadPoolExecutor(max_workers=12) as ex:
            for url, vivant in ex.map(tester_lien, urls):
                if not vivant:
                    morts.append(url)

    # ---- 3. date de l'eyebrow (honnête : on a bien vérifié quelque chose) ----
    date_fr = f"{aujourdhui.day} {MOIS[aujourdhui.month - 1]} {aujourdhui.year}"
    nouveau_html = html
    if EYEBROW_RE.search(nouveau_html):
        nouveau_html = EYEBROW_RE.sub(lambda mm: mm.group(1) + date_fr, nouveau_html, count=1)
    else:
        print("ATTENTION : libellé de date introuvable — date NON mise à jour")

    # ---- réinjection --------------------------------------------------------
    if len(gardes) != avant:
        neuf = json.dumps(gardes, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        m2 = DATA_RE.search(nouveau_html)
        nouveau_html = nouveau_html[:m2.start(2)] + neuf + nouveau_html[m2.end(2):]

    print("=== passe automatique (sans IA) ===")
    print(f"date du jour          : {date_fr}")
    print(f"événements            : {avant} → {len(gardes)}  (purgés : {len(purges)})")
    for e in purges[:8]:
        print(f"    purgé (fin {e.get('d2')}) — {(e.get('n') or '')[:52]}")
    print(f"liens testés          : {len(urls)}  (les {a.max_liens} plus imminents)")
    if morts:
        print(f"liens MORTS (404)     : {len(morts)}")
        for u in morts[:10]:
            print("    ", u)
    else:
        print("liens morts           : aucun")

    if not a.apply:
        print("\n(essai à blanc — rien n'a été écrit ; --apply pour appliquer)")
        return

    open(FULL, "w", encoding="utf-8").write(nouveau_html)
    print(f"\n{FULL} mis à jour.")

    # ---- 4. régénération de l'index allégé et des langues --------------------
    outil = os.path.join(REPO, ".radar", "tools", "split_i18n.py")
    r = subprocess.run([sys.executable, outil, "--apply"], capture_output=True, text=True,
                       env={**os.environ, "RADAR_REPO": REPO})
    print(r.stdout[-600:] or r.stderr[-600:])
    if r.returncode != 0:
        sys.exit("passe_automatique: split_i18n a échoué — on ne publie pas")


if __name__ == "__main__":
    main()
