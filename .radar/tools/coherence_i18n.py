#!/usr/bin/env python3
"""Divergence français / traductions sur les MOIS annoncés.

Incident fondateur (12/08/2026, fiche « Dior Spa Cheval Blanc Paris ») : un
contrôleur avait corrigé le champ français `dt` pour dire la vérité — l'expérience
Dioriviera ne se tient qu'en septembre et novembre 2026 — mais les DOUZE traductions
continuaient d'annoncer « ouvert toute l'année, y compris août 2026 ; collection
estivale en cours ». Un visiteur anglophone lisait donc, ce 12 août, qu'un événement
était en cours alors qu'il n'aurait lieu que six semaines plus tard.

Rien ne l'avait signalé : corriger le français n'invalide pas les traductions, et
aucun filet ne comparait les deux. C'est une divergence muette — la catégorie la plus
dangereuse, parce qu'elle ne casse rien et ne se voit pas depuis le français.

PRINCIPE : un mois affirmé par une traduction doit être légitime, c'est-à-dire cité
par le français OU compris dans la période d1..d2 de la fiche. L'inverse est permis
(une traduction peut condenser). Le français est la source de vérité.

DEUX PIÈGES rencontrés en construisant ce filet, et corrigés ici :

1. « mai » et « may » sont indétectables sans analyse de contexte : « Mayfair »,
   « allocations may be », « maisons de luxe » déclenchaient tous une fausse alerte.
   Le mois de mai n'est donc PAS contrôlé. Limite assumée et écrite, pas masquée.

2. Le lexique et les rangs de mois étaient d'abord deux listes parallèles zippées.
   Ajouter une abréviation d'un côté décalait silencieusement tous les mois suivants.
   Tout est désormais en correspondance explicite mot → numéro de mois.
"""
import datetime as dt
import json
import os
import re
import sys

# Correspondance explicite mot → mois. Aucune liste parallèle : un décalage y serait
# invisible et empoisonnerait tout le contrôle.
MOIS = {
    # Abréviations AVEC et SANS point : les fiches écrivent aussi bien « 2-3 déc. »
    # que « lundis 1er juin-5 oct ». Manquer la forme sans point rendait le français
    # muet sur octobre et faisait accuser dix traductions fidèles.
    "fr": {"janvier": 1, "janv.": 1, "janv": 1, "février": 2, "fevrier": 2, "févr.": 2,
           "fevr.": 2, "févr": 2, "fevr": 2, "mars": 3, "avril": 4, "avr.": 4, "avr": 4,
           "juin": 6, "juillet": 7, "juil.": 7, "juil": 7, "août": 8, "aout": 8,
           "septembre": 9, "sept.": 9, "sept": 9, "octobre": 10, "oct.": 10, "oct": 10,
           "novembre": 11, "nov.": 11, "nov": 11, "décembre": 12, "decembre": 12,
           "déc.": 12, "dec.": 12, "déc": 12, "dec": 12},
    "en": {"january": 1, "february": 2, "march": 3, "april": 4, "june": 6, "july": 7,
           "august": 8, "september": 9, "october": 10, "november": 11, "december": 12},
    "es": {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "junio": 6, "julio": 7,
           "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10, "noviembre": 11,
           "diciembre": 12},
    "it": {"gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "giugno": 6, "luglio": 7,
           "agosto": 8, "settembre": 9, "ottobre": 10, "novembre": 11, "dicembre": 12},
    # « marco » (mars sans accent) est écarté : c'est un prénom courant — « Marco
    # Carola », DJ programmé sur trois fiches, déclenchait un faux mois de mars.
    "pt": {"janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "junho": 6,
           "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11,
           "dezembro": 12},
    "de": {"januar": 1, "februar": 2, "märz": 3, "maerz": 3, "april": 4, "juni": 6,
           "juli": 7, "august": 8, "september": 9, "oktober": 10, "november": 11,
           "dezember": 12},
    "ru": {"январ": 1, "феврал": 2, "март": 3, "апрел": 4, "июн": 6, "июл": 7,
           "август": 8, "сентябр": 9, "октябр": 10, "ноябр": 11, "декабр": 12},
    "ar": {"يناير": 1, "فبراير": 2, "مارس": 3, "أبريل": 4, "يونيو": 6, "يوليو": 7,
           "أغسطس": 8, "سبتمبر": 9, "أكتوبر": 10, "نوفمبر": 11, "ديسمبر": 12},
    "tr": {"ocak": 1, "şubat": 2, "subat": 2, "mart": 3, "nisan": 4, "haziran": 6,
           "temmuz": 7, "ağustos": 8, "agustos": 8, "eylül": 9, "eylul": 9, "ekim": 10,
           # « aralık » (décembre) est écarté : le mot signifie aussi « intervalle »,
           # usage courant qui produisait un faux décembre sur un festival de janvier.
           "kasım": 11, "kasim": 11},
    "hi": {"जनवरी": 1, "फ़रवरी": 2, "फरवरी": 2, "मार्च": 3, "अप्रैल": 4, "जून": 6,
           "जुलाई": 7, "अगस्त": 8, "सितंबर": 9, "अक्टूबर": 10, "नवंबर": 11, "दिसंबर": 12},
}
# Le numéro du mois, écrit tel quel dans ces langues, est le signal le plus fiable.
NUMERIQUE = {"ja": "月", "zh": "月", "ko": "월"}

# Mois hors contrôle, dans TOUTES les langues. Mai y figure parce qu'il est
# indétectable en français et en anglais sans analyse de contexte (voir MOIS) : le
# contrôler dans les langues où il EST détectable ne ferait qu'accuser à tort.
MOIS_NON_CONTROLES = {5}

# Écritures sans notion utile de frontière de mot pour une regex \b.
SANS_FRONTIERE = ("ar", "hi")
# Langues dont le lexique ci-dessus tient en RADICAUX, parce que le mois se décline :
# « сентябр » couvre сентябрь / сентября / сентябре. Leur imposer une frontière à
# droite reviendrait à ne jamais rien trouver — c'est le bug qu'a révélé le test russe.
RADICAUX = ("ru",)


def mois_cites(texte, langue):
    """Numéros des mois nommés dans ce texte, pour cette langue."""
    if not texte:
        return set()
    trouves = set()
    if langue in NUMERIQUE:
        for m in re.finditer(r"(\d{1,2})\s*" + NUMERIQUE[langue], texte):
            n = int(m.group(1))
            if 1 <= n <= 12:
                trouves.add(n)
        return trouves
    bas = texte.lower()
    for mot, rang in MOIS.get(langue, {}).items():
        if langue in SANS_FRONTIERE:
            if mot in texte:
                trouves.add(rang)
            continue
        # Frontières des DEUX côtés : sans la frontière de droite, « Mayfair »
        # déclenchait « may » et « maisons » déclenchait « mai ».
        motif = r"(?<![0-9a-zà-öø-ÿа-яё])" + re.escape(mot)
        if not mot.endswith(".") and langue not in RADICAUX:
            motif += r"(?![a-zà-öø-ÿа-яё])"
        if re.search(motif, bas):
            trouves.add(rang)
    return trouves


def mois_numeriques(texte):
    """Mois écrits en chiffres dans un texte français : « 2026-07-17 », « 17/07/2026 ».

    Sans cette lecture, le français « date NON publiée au 2026-07-17 » paraissait
    muet tandis que sa traduction « as of 17 July 2026 » semblait inventer juillet.
    Onze langues étaient accusées à tort sur une seule fiche.
    """
    if not texte:
        return set()
    mois = set()
    for m in re.finditer(r"\b(?:19|20)\d{2}[-/](\d{1,2})[-/]\d{1,2}\b", texte):
        n = int(m.group(1))
        if 1 <= n <= 12:
            mois.add(n)
    for m in re.finditer(r"\b\d{1,2}[-/](\d{1,2})[-/](?:19|20)\d{2}\b", texte):
        n = int(m.group(1))
        if 1 <= n <= 12:
            mois.add(n)
    # Jour/mois SANS année — « jusqu'au 28/9 », « Polo Exhibition Week 27/07-2/08 ».
    # C'est la forme la plus courante dans les fiches, et celle qui manquait.
    for m in re.finditer(r"(?<![\d/])(\d{1,2})/(\d{1,2})(?![\d/])", texte):
        jour, n = int(m.group(1)), int(m.group(2))
        if 1 <= jour <= 31 and 1 <= n <= 12:
            mois.add(n)
    return mois


def _mois_periode(e):
    """Mois couverts par la période d1..d2 de la fiche — légitimes par construction."""
    def parse(s):
        try:
            return dt.date.fromisoformat((s or "")[:10])
        except Exception:
            return None
    a, b = parse(e.get("d1")), parse(e.get("d2")) or parse(e.get("d1"))
    if not a:
        return set()
    if not b or b < a:
        b = a
    mois, cur = set(), a
    # Bornage : au-delà de 24 mois, la période n'apprend plus rien d'utile.
    while cur <= b and len(mois) <= 24:
        mois.add(cur.month)
        cur = (cur.replace(day=1) + dt.timedelta(days=32)).replace(day=1)
    return mois


def controler(data, champs=("dt", "ds", "p")):
    """Divergences : (nom, langue, champ, mois affirmés sans fondement)."""
    ecarts = []
    for e in data:
        trads = e.get("tr") or {}
        if not trads:
            continue
        periode = _mois_periode(e)
        for champ in champs:
            fr = e.get(champ) or ""
            if not fr:
                continue
            legitimes = mois_cites(fr, "fr") | mois_numeriques(fr) | periode
            if not legitimes:
                continue
            for lg, t in trads.items():
                if lg not in MOIS and lg not in NUMERIQUE:
                    continue
                trad = (t or {}).get(champ) or ""
                if not trad:
                    continue
                # Mai est retiré des DEUX côtés. Il est indétectable en français et en
                # anglais (voir MOIS), mais parfaitement détectable en « 5月 » : sans
                # cette symétrie, toute traduction CJK d'un événement de mai serait
                # accusée d'inventer un mois que le français n'a jamais pu déclarer.
                trop = mois_cites(trad, lg) - legitimes - MOIS_NON_CONTROLES
                if trop:
                    ecarts.append((e.get("n") or "?", lg, champ, sorted(trop)))
    return ecarts


def charger(repo):
    html = open(os.path.join(repo, "index-full.html"), encoding="utf-8").read()
    m = re.search(r'(<script[^>]*id="data"[^>]*>)(.*?)(</script>)', html, re.S)
    return json.loads(m.group(2).replace("<\\/", "</"))


def main():
    repo = os.environ.get("RADAR_REPO") or os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data = charger(repo)
    ecarts = controler(data)
    if not ecarts:
        print(f"OK — {len(data)} fiches, aucune divergence mois français/traduction")
        return 0
    par_fiche = {}
    for nom, lg, champ, trop in ecarts:
        par_fiche.setdefault(nom, []).append((lg, champ, trop))
    print(f"⚠️ {len(par_fiche)} fiche(s), {len(ecarts)} divergence(s) :")
    for nom, lst in sorted(par_fiche.items()):
        langues = sorted({lg for lg, _, _ in lst})
        champs = sorted({c for _, c, _ in lst})
        mois = sorted({m for _, _, t in lst for m in t})
        print(f"  · {nom[:62]}")
        print(f"      mois affirmés sans fondement : {mois} — langues {','.join(langues)} — champs {','.join(champs)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
