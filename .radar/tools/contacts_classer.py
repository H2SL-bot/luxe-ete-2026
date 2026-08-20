# -*- coding: utf-8 -*-
"""Classe une adresse e-mail : voie de SERVICE (a conserver) ou
coordonnee NOMINATIVE d'une personne physique (a retirer du site public).

Principe : on ne devine pas. On croise avec les noms de personnes que le site
a lui-meme enregistres, et on n'ecarte une adresse que sur PREUVE.
"""
import re, json, unicodedata

def sa(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower()

RE_MAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
NOM_RE  = re.compile(r"\b[A-ZÀ-Ý][a-zà-ÿ'’]+(?:[ \-][A-ZÀ-Ý][a-zà-ÿ'’]+){1,2}\b")

ORG = set("""agence agency communication communications management group groupe consulting partners
associates international media relations presse press bureau office studio company societe limited ltd
sas sarl inc llc hotel hotels resort resorts palace club beach house maison chateau villa festival
foundation fondation museum musee institut centre center gallery galerie yacht marina polo golf casino
spa restaurant brasserie collection council chamber federation ville mairie tourisme tourism board
entertainment nightfestival production productions events event gala one beefbar bastide case
lacase stbarth montauk courjardin""".split())

# Fournisseurs de messagerie GRAND PUBLIC : une adresse chez eux est, par
# construction, l'adresse privee d'une personne — jamais une boite de service.
PERSO = set("""gmail.com googlemail.com hotmail.com hotmail.fr outlook.com outlook.fr live.com
live.fr msn.com yahoo.com yahoo.fr ymail.com icloud.com me.com mac.com aol.com free.fr orange.fr
wanadoo.fr sfr.fr laposte.net bbox.fr numericable.fr protonmail.com proton.me gmx.com gmx.fr
web.de mail.ru yandex.ru qq.com 163.com libero.it virgilio.it tiscali.it alice.it""".split())

SERVICE = set("""press presse pressoffice media medias info infos information contact contacts contactez
rsvp reservation reservations resa booking bookings billetterie billets tickets ticketing boxoffice
guichet accreditation accreditations concierge conciergerie sales vente ventes commercial communication
comms dircom secretariat admin administration office bureau general generale enquiries inquiries support
service services client clients customer clientele event events evenement evenements entertainment
marketing partenariat partenariats partnership partnerships sponsoring mecenat gala galas adhesion
membership abonnement abonnements groupe groupes groups visites visiteurs visitors tourisme tourism
boutique shop store magasin restaurant dining spa wellness hotel hotels resort club house festival
museum musee fondation foundation agence agency team equipe staff mail email courriel newsletter
noreply webmaster postmaster direction welcome hello bonjour ciao hola accueil reception standard
artistique culture culturel programme agenda demande demandes pole cellule night nightfestival
secretaire secretary relations relation public publics privatisation privatisations""".split())

def personnes_de_la_fiche(iv, stricte=False):
    """Noms de personnes que la fiche enregistre. stricte=True : uniquement
    les entrees explicitement typees « nom »."""
    out = []
    if not isinstance(iv, dict) or not isinstance(iv.get("c"), list):
        return out
    for it in iv["c"]:
        if not isinstance(it, dict):
            continue
        champs = []
        if str(it.get("t", "")).strip().lower() in ("nom", "fonction"):
            champs.append(str(it.get("v", "")))
        if not stricte:
            champs.append(str(it.get("t", "")))
        for s in champs:
            s = re.split(r"[—(]", s)[0]
            for m in NOM_RE.finditer(s):
                mots = m.group(0).replace("-", " ").split()
                if 2 <= len(mots) <= 3 and not any(sa(w) in ORG for w in mots):
                    out.append([sa(w) for w in mots])
    return out

def construire_vocabulaire(ev):
    """Prenoms et patronymes attestes par le site (entrees « nom » seulement)."""
    prenoms, patronymes = set(), set()
    for e in ev:
        for p in personnes_de_la_fiche(e.get("iv") or {}, stricte=True):
            prenoms.add(p[0])
            patronymes.update(p[1:])
    return prenoms, patronymes

def vocabulaire_lieux(ev):
    """Mots de lieu attestes par le site (villes, lieux, titres de fiche) :
    ils ne doivent jamais etre pris pour des patronymes."""
    v = set()
    for e in ev:
        for champ in ("v", "l", "n"):
            for mot in re.split(r"[^A-Za-zÀ-ÿ]+", str(e.get(champ) or "")):
                if len(mot) >= 3:
                    v.add(sa(mot))
                    v.add(sa(mot).replace("saint", "st"))
    return v

def classer(adr, pers_fiche, prenoms, patronymes, lieux=frozenset()):
    """Retourne None si l'adresse est conservee, sinon le motif du retrait."""
    dom = sa(adr.split("@", 1)[1]) if "@" in adr else ""
    loc = sa(adr.split("@")[0])
    jetons = [t for t in re.split(r"[._\-+0-9]+", loc) if len(t) > 1]
    if any(t in SERVICE for t in jetons):
        return None
    # D — messagerie grand public : adresse privee d'une personne, sans exception
    if dom in PERSO:
        return "D"
    # A — une personne est nommee sur la fiche meme
    for p in pers_fiche:
        if len(set(jetons) & set(p)) >= 2 or loc in ("".join(p), p[0],
               p[0][0] + "." + p[-1], p[0][0] + p[-1], p[0] + "." + p[-1]):
            return "A"
    parts = [t for t in re.split(r"[._\-]", loc) if t]
    # B — forme « prenom.nom ». On ecarte ce qui est un nom de LIEU atteste
    # par le site (Lacase.stbarth, beachclub.montauk…), qui sont des boites
    # de service et non des personnes.
    if len(parts) == 2 and all(t.isalpha() for t in parts):
        if any(t in lieux for t in parts):
            return None
        if 3 <= len(parts[0]) <= 14 and 3 <= len(parts[1]) <= 16:
            return "B"
        if len(parts[0]) == 1 and 4 <= len(parts[1]) <= 16 and parts[1] in patronymes:
            return "B"
    # C — prenom seul, atteste par le site
    if len(parts) == 1 and loc in prenoms and loc not in patronymes:
        return "C"
    return None
