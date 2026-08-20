# -*- coding: utf-8 -*-
"""Retire du site PUBLIC les coordonnees nominatives des personnes physiques.

Ce qui part : l'adresse e-mail d'une personne, et la ligne directe d'une
personne. Ce qui reste : le nom et la fonction (information editoriale
legitime, publiee par les sources officielles) et TOUTES les voies de
service — press@, info@, rsvp@, standards, billetteries, formulaires.

GARDE-FOU : une fiche ne perd jamais sa derniere porte d'entree. Si le
nettoyage devait la laisser sans aucune voie, la fiche est laissee intacte
et signalee — la LOI DU SITE prime sur le nettoyage.

Usage :  python3 nettoyer.py --blanc    (essai, n'ecrit rien)
         python3 nettoyer.py --appliquer
"""
import re, json, sys, glob, os, unicodedata, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contacts_classer as C

RE_TEL = re.compile(r"(?:\+\d[\d ().\-]{7,}\d)|(?:\b0\d[\d ().\-]{8,}\d)")
LIGNE_DIRECTE = re.compile(r"ligne directe|direct line|ligne perso", re.I)

# ── vocabulaire, construit une seule fois sur la version francaise ──────────
def vocabulaire(ev):
    prenoms, patronymes = C.construire_vocabulaire(ev)
    lieux = C.vocabulaire_lieux(ev)
    return prenoms, patronymes, lieux

# Registre des adresses jugees nominatives pendant la passe francaise. Les
# traductions n'ont pas les entrees « nom » de la fiche : la regle A ne peut
# pas s'y appliquer. On leur transmet donc le verdict deja rendu sur le
# francais, pour qu'une adresse retiree ici le soit dans les 13 langues.
NOMINATIVES = set()

def nominative(adr, pers, voc):
    if adr.lower() in NOMINATIVES:
        return True
    r = C.classer(adr, pers, voc[0], voc[1], voc[2]) is not None
    if r:
        NOMINATIVES.add(adr.lower())
    return r

def cite_une_personne(txt, pers):
    """Le texte nomme-t-il explicitement une personne attestee sur la fiche ?"""
    t = C.sa(txt or "")
    for p in pers:
        if all(re.search(r"\b" + re.escape(w) + r"\b", t) for w in p):
            return True
    return False

# ── nettoyage d'un texte libre ─────────────────────────────────────────────
# On ne retouche QUE le voisinage immediat de l'adresse retiree. Un recollage
# global cassait la typographie francaise (l'espace avant « : » « ; » « » »),
# y compris a des centaines de caracteres du retrait : bug constate a l'essai.
_M = r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
MOTIFS = [
    # « (contact@…) » ou « (e-mail : contact@…) » — parenthese entiere
    re.compile(r"\s*\(\s*(?:e-?mails?\s*:?\s*|courriel\s*:?\s*)?(" + _M + r")\s*\)"),
    # « — contact@… » / « – contact@… »
    re.compile(r"\s*[—–]\s*(" + _M + r")(?=[\s.,;:)»]|$)"),
    # « , contact@… » / « ; contact@… »
    re.compile(r"\s*[,;]\s*(" + _M + r")(?=[\s.,;:)»]|$)"),
    # « contact@…, » / « contact@… ; »
    re.compile(r"(" + _M + r")\s*[,;]\s*"),
    # adresse nue
    re.compile(r"\s*(" + _M + r")"),
]

# Numero PERSONNEL dans un texte libre : portable francais (06/07, +33 6/7)
# ou numero explicitement presente comme mobile / ligne directe. Les standards
# et les lignes de billetterie ne sont jamais touches.
RE_MOBILE_FR = re.compile(r"(?:\+33\s?\(?0?\)?\s?[67]|\b0[67])[\d ().\-]{8,}\d")
RE_NUM = re.compile(r"(?:\+\d[\d ().\-]{7,}\d)|(?:\b0\d[\d ().\-]{8,}\d)")
MARQUEUR_PERSO = re.compile(r"mobile|portable|ligne directe|direct line|cell\b|gsm", re.I)

def retire_numeros_personnels(t, pers):
    """Retire les portables attaches a une personne nommee, clause par clause.
    On travaille par segments (« ; » et « . ») pour ne jamais retirer le
    standard d'un lieu cite dans la meme phrase."""
    if not pers or not RE_NUM.search(t or ""):
        return t, 0
    n = 0
    morceaux = re.split(r"(\s*;\s*|(?<=[a-z0-9)])\.\s+)", t)
    sortie = []
    for seg in morceaux:
        if not cite_une_personne(seg, pers):
            sortie.append(seg); continue
        perso = bool(MARQUEUR_PERSO.search(seg))
        def r(m):
            nonlocal n
            est_mobile = bool(RE_MOBILE_FR.match(m.group(0).strip()))
            if not (est_mobile or perso):
                return m.group(0)
            n += 1
            return "\x00"
        seg = RE_NUM.sub(r, seg)
        if "\x00" in seg:
            seg = re.sub(r"\s*\(\s*(?:mobile|portable|tel\.?|t[ée]l[ée]phone)?\s*\x00\s*\)", "", seg)
            seg = re.sub(r"\s*[,;—–]\s*(?:mobile|portable)?\s*\x00", "", seg)
            seg = re.sub(r"\s*(?:mobile|portable)?\s*\x00", "", seg)
            seg = re.sub(r"\(\s*\)", "", seg)
            seg = re.sub(r"[ \t]{2,}", " ", seg)
            seg = re.sub(r"\s+([,.])(?!\d)", r"\1", seg)
        sortie.append(seg)
    return "".join(sortie), n

def nettoie_texte(t, pers, voc):
    if not isinstance(t, str):
        return t, 0
    n0 = 0
    if pers:
        t, n0 = retire_numeros_personnels(t, pers)
    if "@" not in t:
        return t, n0
    n = n0
    def faire(motif):
        nonlocal n
        def r(m):
            nonlocal n
            if nominative(m.group(1), pers, voc):
                n += 1
                return ""
            return m.group(0)
        return motif.sub(r, t)
    for motif in MOTIFS:
        t = faire(motif)
    if n:
        # reparations strictement locales, sans toucher a la ponctuation francaise
        t = re.sub(r"\(\s*\)", "", t)                 # parenthese devenue vide
        t = re.sub(r"[ \t]{2,}", " ", t)               # double espace laisse par le retrait
        t = re.sub(r"\s+([,.])(?!\d)", r"\1", t)       # espace avant virgule/point seulement
        t = re.sub(r"(?<![.:])\s*:\s*(?=[.;]|$)", "", t)  # deux-points devenu orphelin
        t = re.sub(r"\s+$", "", t)
    return t, n

# ── nettoyage recursif de toute valeur (str / list / dict) ─────────────────
def nettoie_valeur(v, pers, voc, journal, fiche, chemin):
    if isinstance(v, str):
        nv, n = nettoie_texte(v, pers, voc)
        if n:
            journal.append({"fiche": fiche, "ou": chemin, "type": "e-mail (texte)", "n": n})
        return nv, n
    if isinstance(v, list):
        out, tot = [], 0
        for i, x in enumerate(v):
            nx, n = nettoie_valeur(x, pers, voc, journal, fiche, f"{chemin}[{i}]")
            out.append(nx); tot += n
        return out, tot
    if isinstance(v, dict):
        out, tot = {}, 0
        for k, x in v.items():
            nx, n = nettoie_valeur(x, pers, voc, journal, fiche, f"{chemin}.{k}")
            out[k] = nx; tot += n
        return out, tot
    return v, 0

# ── contacts structures : on retire l'ENTREE entiere ───────────────────────
def nettoie_contacts(liste, pers, voc, journal, fiche, retires):
    garde, n = [], 0
    for it in liste:
        if not isinstance(it, dict):
            garde.append(it); continue
        t, v = str(it.get("t") or ""), str(it.get("v") or "")
        mails = C.RE_MAIL.findall(v)
        motif = None
        if mails and all(nominative(a, pers, voc) for a in mails):
            motif = "e-mail nominatif"
        elif RE_TEL.search(v) and (LIGNE_DIRECTE.search(t + " " + v)
                                   or cite_une_personne(t + " " + v, pers)):
            motif = "ligne directe d'une personne"
        if motif:
            n += 1
            retires.append({"fiche": fiche, "motif": motif, "libelle": t, "valeur": v})
            journal.append({"fiche": fiche, "ou": "iv.c", "type": motif, "n": 1})
        else:
            garde.append(it)
    return garde, n

def a_une_porte(iv, sej):
    if isinstance(iv, dict):
        if any((iv.get(k) or "").strip() for k in ("o", "g", "w")):
            return True
        if iv.get("c"):
            return True
    if isinstance(sej, dict) and any(sej.get(k) for k in ("hotels", "tables", "exp", "pitch")):
        return True
    return False

# ══════════════════════════════════════════════════════════════════════════
def main():
    mode = "--appliquer" if "--appliquer" in sys.argv else "--blanc"
    # DOCTRINE « OÙ VIT LA VÉRITÉ » : index.html et i18n-data/ sont GÉNÉRÉS.
    # La source de travail est index-full.html, qui porte aussi les traductions
    # dans e.tr.<langue>. Éditer index.html directement ne sert à rien : le
    # premier split_i18n.py écrase la modification (constaté le 20/08/2026).
    if not os.path.exists("index-full.html"):
        os.system("python3 .radar/tools/rebuild_full.py >/dev/null")
    html = open("index-full.html", encoding="utf-8").read()
    m = re.search(r'(<script type="application/json" id="data">)(.*?)(</script>)', html, re.S)
    ev = json.loads(m.group(2))
    voc = vocabulaire(ev)

    journal, retires, sauves = [], [], []
    total = 0
    for e in ev:
        fiche = e.get("n") or "?"
        pers = C.personnes_de_la_fiche(e.get("iv") or {})
        avant = json.dumps(e, ensure_ascii=False)
        n = 0
        iv = e.get("iv")
        if isinstance(iv, dict) and isinstance(iv.get("c"), list):
            iv["c"], k = nettoie_contacts(iv["c"], pers, voc, journal, fiche, retires)
            n += k
        for champ in list(e.keys()):
            if champ in ("n", "d1", "d2", "u", "v", "l", "z", "g", "c", "a"):
                continue
            nv, k = nettoie_valeur(e[champ], pers, voc, journal, fiche, champ)
            e[champ] = nv; n += k
        if n and not a_une_porte(e.get("iv"), e.get("sej")):
            e.clear(); e.update(json.loads(avant))
            sauves.append(fiche)
            n = 0
        total += n

    # Les traductions vivent dans e.tr.<langue> et ont donc deja ete nettoyees
    # par la boucle ci-dessus, avec les MEMES personnes que la version francaise.
    print(f"  (adresses jugees nominatives : {len(NOMINATIVES)})")
    trad = {}

    # ── rapport ────────────────────────────────────────────────────────────
    par_type = collections.Counter(j["type"] for j in journal)
    print(f"  MODE : {'APPLICATION' if mode=='--appliquer' else 'ESSAI À BLANC (rien n’est écrit)'}")
    print()
    print(f"  Coordonnées retirées au total ………………… {total}")
    for t, n in par_type.most_common():
        print(f"    · {t:<32} {n}")
    print()
    print(f"  Fiches touchées …………………………………………… {len({j['fiche'] for j in journal})}")
    print(f"  Fiches épargnées par le garde-fou ……………… {len(sauves)}")
    for s in sauves[:6]:
        print(f"      ⚠️  {s[:64]}")
    if mode != "--appliquer":
        json.dump(retires, open("/tmp/retires.json", "w"), ensure_ascii=False, indent=1)
        print("\n  (essai — aucun fichier modifié)")
        return
    # ── ecriture ───────────────────────────────────────────────────────────
    neuf = json.dumps(ev, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    open("index-full.html", "w", encoding="utf-8").write(
        html[:m.start(2)] + neuf + html[m.end(2):])
    json.dump(retires, open("/tmp/retires.json", "w"), ensure_ascii=False, indent=1)
    print("\n  ✓ index-full.html réécrit (source de vérité)")
    print("  → lancer ensuite : python3 .radar/tools/split_i18n.py --apply")

main()
