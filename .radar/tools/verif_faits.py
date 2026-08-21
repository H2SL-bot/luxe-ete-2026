#!/usr/bin/env python3
# verif_faits.py — contrôle mécanique de non-perte de faits durs (e-mails, URLs,
# téléphones, montants) entre un texte AVANT et un texte APRÈS (condensation,
# réécriture...). Ne jamais accepter "rien n'a été perdu" sur la parole de
# l'agent qui a fait le travail (leçon du 20/08/2026) : ce script le vérifie.
#
# Usage : python3 verif_faits.py <dossier_entree> <dossier_sortie>
#   - dossier_entree/*.json et dossier_sortie/*.json : fichiers appariés par le
#     champ "n" (nom de la fiche), pas par nom de fichier ni position.
#   - chaque fichier contient au moins {"n": ..., "o": ..., "g": ..., "w": ...}
#     (ou tout sous-ensemble de champs texte à comparer — adapter FIELDS si besoin).
import json, re, sys, glob

FIELDS = ("o", "g", "w")

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
URL_RE = re.compile(r'https?://[^\s")\]<>]+|(?<![\w@])[a-zA-Z0-9\-]+\.(?:com|org|net|fr|it|co|io)/[^\s")\]<>]*', re.I)
PHONE_RE = re.compile(r'(?:\+\d{1,3}[\s.\-]?)?\(?0?\d\)?(?:[\s.\-]?\d{2}){4,5}')
MONEY_RE = re.compile(r'\d[\d\s.,]*\s?(?:€|EUR|USD|\$|CHF|£)', re.I)

def norm_phone_variants(s):
    digits = re.sub(r'[^\d]', '', s)
    # variantes possibles : le numéro entier, et sa terminaison à 9 chiffres
    # (pour absorber +33/0 en tête, source de faux positifs récurrente).
    variants = {digits}
    if len(digits) >= 9:
        variants.add(digits[-9:])
    return variants

def norm_money(s):
    # ignore les zéros de centimes (115,00 € == 115 €) et les zéros de tête.
    digits = re.sub(r'[^\d]', '', s)
    if len(digits) > 2 and digits.endswith("00"):
        digits = digits[:-2]
    return digits.lstrip('0') or '0'

def norm_email(s):
    return s.strip('.,;:)').lower()

def norm_url(s):
    u = s.strip('.,;:)').lower()
    u = re.sub(r'^https?://(www\.)?', '', u)
    return u.rstrip('/')

def extract(text):
    emails = {norm_email(e) for e in EMAIL_RE.findall(text)}
    urls = {norm_url(u) for u in URL_RE.findall(text)}
    phones_raw = [p for p in PHONE_RE.findall(text) if len(re.sub(r'[^\d]', '', p)) >= 9]
    phones = set()
    for p in phones_raw:
        phones |= norm_phone_variants(p)
    moneys = {norm_money(m) for m in MONEY_RE.findall(text)}
    return emails, urls, phones, moneys

def check(old_text, new_text):
    oe, ou, op, om = extract(old_text)
    ne, nu, np_, nm = extract(new_text)
    problems = []
    if oe - ne: problems.append(f"emails perdus: {oe - ne}")
    if ou - nu: problems.append(f"urls perdues: {ou - nu}")
    # un numéro n'est "perdu" que si NI le numéro entier NI sa terminaison
    # à 9 chiffres ne survit quelque part dans le texte neuf.
    lost_phones = {p for p in op if p not in np_ and not any(p.endswith(x) or x.endswith(p) for x in np_)}
    if lost_phones: problems.append(f"telephones perdus: {lost_phones}")
    if om - nm: problems.append(f"montants perdus: {om - nm}")
    return problems

def main(dir_in, dir_out):
    entries = {}
    for fn in glob.glob(f"{dir_in}/*.json"):
        e = json.load(open(fn, encoding="utf-8"))
        entries[e["n"]] = e

    all_ok = True
    for fn in sorted(glob.glob(f"{dir_out}/*.json")):
        out = json.load(open(fn, encoding="utf-8"))
        name = out.get("n")
        cand = entries.get(name)
        if not cand:
            print(f"{fn}: NOM INTROUVABLE dans {dir_in} ({(name or '')[:50]})")
            all_ok = False
            continue
        old_concat = " ".join(cand.get(f, "") or "" for f in FIELDS)
        new_concat = " ".join(out.get(f, "") or "" for f in FIELDS)
        problems = check(old_concat, new_concat)
        status = "OK" if not problems else "ALERTE"
        if problems:
            all_ok = False
        print(f"[{status}] {fn} — {name[:55]}")
        for p in problems:
            print(f"    - {p}")
    print()
    print("TOUT OK" if all_ok else "DES PERTES DETECTEES — a examiner au cas par cas")
    return 0 if all_ok else 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: verif_faits.py <dossier_entree> <dossier_sortie>")
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
