#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
relever_visites.py — un relevé par jour du compteur de visites du site.

Pourquoi : les statistiques (GoatCounter) sont publiques mais ne donnent que le
cumul de l'instant. Pour dire chaque matin « +N visites depuis hier » — dans le
bulletin quotidien et sur le tableau de bord public — il faut une mémoire :
une ligne par jour dans stats/visites.ndjson.

Qui l'appelle : le plancher (passe-quotidienne.yml), et la routine Claude si
le relevé du jour manque. Jamais deux lignes pour le même jour.

Ce fichier vit dans stats/ (et pas .radar/) car GitHub Pages ne sert pas les
dossiers commençant par un point : le tableau de bord public doit pouvoir le lire.
"""
import datetime
import json
import os
import re
import sys
import urllib.request

REPO = os.environ.get("RADAR_REPO") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FICHIER = os.path.join(REPO, "stats", "visites.ndjson")
COMPTEUR = "https://constanceparis7.goatcounter.com/counter/TOTAL.json"


def nombre(s):
    """GoatCounter renvoie des chaînes parfois formatées (« 1 234 ») : on nettoie."""
    n = re.sub(r"[^0-9]", "", str(s))
    if not n:
        raise ValueError(f"pas un nombre : {s!r}")
    return int(n)


def main():
    jour = datetime.date.today().isoformat()
    os.makedirs(os.path.dirname(FICHIER), exist_ok=True)

    if os.path.exists(FICHIER) and f'"date": "{jour}"' in open(FICHIER, encoding="utf-8").read():
        print(f"relevé du {jour} déjà présent — rien à faire")
        return

    try:
        with urllib.request.urlopen(COMPTEUR, timeout=25) as r:
            d = json.loads(r.read())
        visiteurs = nombre(d["count_unique"])
        pages = nombre(d["count"])
    except Exception as e:
        # Compteur illisible = pas grave : on n'écrit rien, on reprendra demain.
        # Surtout ne pas faire échouer la passe pour une statistique.
        print(f"compteur illisible aujourd'hui ({e}) — on n'écrit rien")
        return

    with open(FICHIER, "a", encoding="utf-8") as f:
        f.write(json.dumps({"date": jour, "visites": visiteurs, "pages": pages}) + "\n")
    print(f"relevé du {jour} : {visiteurs} visiteurs, {pages} pages vues")


if __name__ == "__main__":
    main()
