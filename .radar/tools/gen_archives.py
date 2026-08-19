#!/usr/bin/env python3
"""Construit archives.json — la mémoire du radar.

Décision de Gérald, 12/08/2026 : « Je veux que ce qui existait […] disparaisse
automatiquement de la page classement prestige […] mais qu'ils soient transférés dans
une rubrique archives pour que tout le travail qui a été effectué serve à quelque chose
et que les gens voient que c'est un site de référence internationale. » Et, précision du
même jour : « L'archive, tous les séjours que tu as créés depuis le début. Je ne veux pas
que tu commences les archives uniquement maintenant. »

L'archive est donc RÉTROACTIVE. Deux gisements :

1. Les fiches actuellement en ligne dont la date de fin est passée.
2. Les fiches PURGÉES au fil des mois — la purge des zombies retire du site tout
   événement fini depuis plus de trente jours. Elles n'existent plus nulle part sauf
   dans l'historique Git de index.html, qu'on relit ici commit par commit.

Le fichier produit est servi À PART et chargé seulement quand le visiteur ouvre la
rubrique : l'archive peut grossir indéfiniment sans jamais alourdir la page d'accueil,
ce qui respecte le mandat de vitesse mobile.

Champs conservés : le strict nécessaire pour montrer qu'un événement a existé et de
quoi il s'agissait. Ni traductions, ni séjour, ni voie d'invitation — l'archive est une
preuve de travail, pas un service.
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys

REPO = os.environ.get("RADAR_REPO") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHAMPS = ("n", "d1", "d2", "v", "l", "c", "z", "g", "u", "sw", "sv")


def _data_de(blob):
    m = re.search(r'id="data">(.*?)</script>', blob, re.S)
    if not m:
        return []
    try:
        return json.loads(m.group(1).replace("<\\/", "</"))
    except Exception:
        return []


def _garder(e):
    return {k: e.get(k) for k in CHAMPS if e.get(k) not in (None, "")}


def collecter(verbeux=True):
    """Toutes les fiches ayant existé, la version la plus riche de chacune."""
    vus = {}
    courant = _data_de(open(os.path.join(REPO, "index-full.html"), encoding="utf-8").read())
    for e in courant:
        if e.get("n"):
            vus[e["n"]] = _garder(e)
    vivants = set(vus)

    revs = subprocess.run(["git", "-C", REPO, "log", "--format=%H", "--", "index.html"],
                          capture_output=True, text=True).stdout.split()
    for i, h in enumerate(revs):
        blob = subprocess.run(["git", "-C", REPO, "show", f"{h}:index.html"],
                              capture_output=True, text=True).stdout
        for e in _data_de(blob):
            n = e.get("n")
            if not n:
                continue
            neuf = _garder(e)
            # On garde la version la plus complète rencontrée : les fiches
            # s'enrichissent au fil des passes, l'archive mérite la meilleure.
            if n not in vus or len(json.dumps(neuf, ensure_ascii=False)) > len(
                    json.dumps(vus[n], ensure_ascii=False)):
                if n not in vivants or n not in vus:
                    vus[n] = neuf
        if verbeux and i % 40 == 0:
            print(f"   ...{i + 1}/{len(revs)} commits — {len(vus)} fiches", flush=True)
    return vus, vivants


def main():
    aujourdhui = dt.date.today().isoformat()
    vus, vivants = collecter()

    archives = []
    for n, e in vus.items():
        fin = e.get("d2") or e.get("d1") or ""
        if not fin or fin >= aujourdhui:
            continue          # pas encore terminé : sa place est dans le classement
        e = dict(e)
        e["ret"] = n not in vivants   # retirée du site (purgée) ou simplement passée
        archives.append(e)

    archives.sort(key=lambda e: (e.get("d2") or e.get("d1") or ""), reverse=True)
    sortie = os.path.join(REPO, "archives.json")
    json.dump({"maj": aujourdhui, "total": len(archives), "ev": archives},
              open(sortie, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

    purgees = sum(1 for e in archives if e.get("ret"))
    poids = os.path.getsize(sortie) / 1024
    print(f"archives.json : {len(archives)} événements terminés — {poids:.0f} Ko")
    print(f"   dont {purgees} retrouvés dans l'historique Git (retirés du site depuis)")
    print(f"   et {len(archives) - purgees} encore en ligne mais terminés")
    if archives:
        print(f"   du {archives[-1].get('d2')} au {archives[0].get('d2')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
