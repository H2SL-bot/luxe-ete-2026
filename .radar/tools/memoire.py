#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""memoire.py — la Mémoire du radar (fondée le 27/08/2026).

Le vrai trésor du site n'est pas ce qu'il sait, c'est DEPUIS QUAND il le
sait : personne ne peut racheter le temps. Ce module tient le registre
`.radar/memoire.ndjson` (append-only, jamais réécrit) :

  {"date": "2026-08-27", "type": "...", "evenement": "<nom EXACT de fiche>",
   "detail": "...", "preuve": "..."}

Types :
  - changement_date : d1/d2 d'une fiche a bougé (détecté ici, via git)
  - fenetre_annoncee : une ouverture de billetterie/réservation est annoncée
  - fenetre_ouverte  : la vente/réservation a réellement ouvert
  - complet          : épuisement constaté, avec le délai si mesurable
  - observation      : fait daté digne de mémoire, avec sa preuve

Usage :
  python3 memoire.py changements [--jours 7]   # détecte et consigne les
      dates qui ont bougé depuis N jours (compare l'index.html d'alors,
      via l'historique git, à celui d'aujourd'hui ; appariement par NOM
      EXACT ; jamais de doublon : une même bascule n'est consignée qu'une fois)
  python3 memoire.py ajouter --type T --evenement N --detail D --preuve P
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date

RAD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(RAD)
REGISTRE = os.path.join(RAD, "memoire.ndjson")


def _data(texte):
    m = re.search(r'<script type="application/json" id="data">(.*?)</script>', texte, re.S)
    return json.loads(m.group(1)) if m else []


def _charger_registre():
    if not os.path.exists(REGISTRE):
        return []
    out = []
    for ligne in open(REGISTRE, encoding="utf-8"):
        ligne = ligne.strip()
        if ligne:
            try:
                out.append(json.loads(ligne))
            except json.JSONDecodeError:
                pass
    return out


def _ecrire(entree):
    with open(REGISTRE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")


def changements(jours):
    ref = subprocess.run(
        ["git", "rev-list", "-1", f"--before={jours} days ago", "HEAD", "--", "index.html"],
        capture_output=True, text=True, cwd=REPO).stdout.strip()
    if not ref:
        print(f"memoire: aucun commit d'index.html vieux de {jours} jours — rien à comparer")
        return 0
    avant = _data(subprocess.run(["git", "show", f"{ref}:index.html"],
                                 capture_output=True, text=True, cwd=REPO).stdout)
    apres = _data(open(os.path.join(REPO, "index.html"), encoding="utf-8").read())
    A = {f.get("n"): f for f in avant}
    B = {f.get("n"): f for f in apres}
    deja = {(e.get("evenement"), e.get("detail")) for e in _charger_registre()
            if e.get("type") == "changement_date"}
    n = 0
    for nom in sorted(set(A) & set(B)):
        av, ap = A[nom], B[nom]
        if (av.get("d1"), av.get("d2")) == (ap.get("d1"), ap.get("d2")):
            continue
        detail = (f"{av.get('d1')} → {av.get('d2')} devient "
                  f"{ap.get('d1')} → {ap.get('d2')}")
        if (nom, detail) in deja:
            continue
        _ecrire({"date": date.today().isoformat(), "type": "changement_date",
                 "evenement": nom, "detail": detail,
                 "preuve": f"historique git du site (référence {ref[:9]})"})
        print(f"  ± {nom[:64]} : {detail}")
        n += 1
    print(f"memoire: {n} changement(s) de dates consigné(s) sur {jours} jours")
    return n


def ajouter(args):
    if args.type not in ("fenetre_annoncee", "fenetre_ouverte", "complet", "observation"):
        sys.exit("memoire: type inconnu")
    _ecrire({"date": date.today().isoformat(), "type": args.type,
             "evenement": args.evenement, "detail": args.detail, "preuve": args.preuve})
    print("memoire: consigné")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("changements")
    c.add_argument("--jours", type=int, default=7)
    a = sub.add_parser("ajouter")
    a.add_argument("--type", required=True)
    a.add_argument("--evenement", required=True)
    a.add_argument("--detail", required=True)
    a.add_argument("--preuve", required=True)
    args = ap.parse_args()
    if args.cmd == "changements":
        changements(args.jours)
    else:
        ajouter(args)
