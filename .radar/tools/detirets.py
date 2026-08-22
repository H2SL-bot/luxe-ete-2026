# -*- coding: utf-8 -*-
"""Retire les tirets longs employés comme PONCTUATION (— et –), qui signent
une écriture automatique quand ils sont aussi denses, et conserve :
  - les traits d'union des mots composés (Saint-Tropez, week-end, jet-set) ;
  - les demi-cadratins entre chiffres (1941–1954, 5–11 avril), qui sont de la
    bonne typographie française et non un tic d'IA — et dont dépend au moins
    une adresse de page.
"""
import re

CAD = "—"   # —
DEMI = "–"  # –

# 1941–1954, 5–11, 12h–14h : on garde, c'est correct et une URL en dépend.
_PLAGE = re.compile(r"(?<=[0-9hH])\s*" + DEMI + r"\s*(?=[0-9])")

def _protege(t):
    return _PLAGE.sub("\x01", t)

def _rend(t):
    return t.replace("\x01", DEMI)

def titre(t):
    """Un titre : « Lieu — sujet » devient « Lieu, sujet ». La virgule est le
    séparateur le plus neutre en français ; le deux-points serait un autre tic."""
    if not isinstance(t, str):
        return t
    t = _protege(t)
    t = re.sub(r"\s*[" + CAD + DEMI + r"]\s*", ", ", t)
    t = re.sub(r",\s*,", ",", t)
    t = re.sub(r"\s+,", ",", t)
    return _rend(t)

def texte(t):
    """Un texte courant. Trois cas, du plus précis au plus général."""
    if not isinstance(t, str) or (CAD not in t and DEMI not in t):
        return t
    t = _protege(t)
    d = "[" + CAD + DEMI + "]"

    # a0) un deux-points precede deja le tiret : le tiret est redondant, on le
    #     supprime purement. Sinon on fabriquait « la Maison :, store@... ».
    t = re.sub(r"(:)\s*" + d + r"\s*", r"\1 ", t)

    # a) incise encadrée : « mot — aparté — suite » → virgules
    t = re.sub(r"\s*" + d + r"\s*([^" + CAD + DEMI + r"]{3,90}?)\s*" + d + r"\s*",
               r", \1, ", t)

    # b) le tiret introduit une proposition complète (sujet + verbe conjugué
    #    fréquent) : on coupe la phrase. « X — c'est Y » → « X. C'est Y »
    def coupe(m):
        suite = m.group(1)
        return ". " + suite[0].upper() + suite[1:]
    t = re.sub(r"\s*" + d + r"\s+((?:c'est|ce n'est|il|elle|on|c’est)\b[^.]{0,120}\.)",
               coupe, t)

    # c) reste. Trois situations, dans cet ordre :
    #    - à l'intérieur d'une parenthèse : TOUJOURS une virgule (un deux-points
    #      dans une parenthèse qui en contient déjà un est illisible) ;
    #    - une proposition indépendante suit : on coupe la phrase, sinon on
    #      fabrique une virgule qui colle deux phrases (faute constatée à l'essai) ;
    #    - sinon : deux-points s'il n'y en a pas déjà, virgule sinon.
    INDEP = re.compile(r"^(les|la|le|l'|il|elle|on|ils|elles|un|une|cette|ces|"
                       r"leur|leurs|son|sa|ses|c'est|ce n'est|chaque|tout|toute)\s+"
                       r"[^.]{0,140}?\b(est|sont|monte|montent|reste|restent|"
                       r"permet|permettent|donne|donnent|ouvre|ouvrent|ferme|"
                       r"ferment|commence|commencent|vaut|valent|peut|peuvent|"
                       r"doit|doivent|fait|font|a|ont)\b", re.I)

    def general(m):
        avant = t[:m.start()]
        apres = t[m.end():]
        # Une fin de phrase, c'est un point SUIVI D'UNE ESPACE. Chercher un
        # point nu faisait passer « summergalabygalaone.org » pour une fin de
        # phrase, et le repérage des parenthèses tombait à côté.
        dernier = max((avant.rfind(x) for x in (". ", "! ", "? ", "\n")), default=-1)
        phrase = avant[dernier + 1:]
        # dans une parenthèse ouverte ?
        if phrase.count("(") > phrase.count(")"):
            return ", "
        if INDEP.match(apres.lstrip()):
            suite = apres.lstrip()
            return ". \x02"          # marque : la suite prend une majuscule
        return " : " if ":" not in phrase else ", "
    t = re.sub(r"\s*" + d + r"\s*", general, t)
    # applique les majuscules demandées par les coupures
    t = re.sub(r"\x02(.)", lambda m: m.group(1).upper(), t)

    # nettoyage local
    t = re.sub(r"\s+([,.])(?!\d)", r"\1", t)
    t = re.sub(r"([,;:])\s*\1+", r"\1", t)
    t = re.sub(r":\s*:", ":", t)
    # Un deux-points ou un point-virgule suivi d'une virgule : la virgule est
    # redondante. Cas produit quand la ponctuation d'origine bordait deja le tiret.
    t = re.sub(r"([:;])\s*,\s*", r"\1 ", t)
    t = re.sub(r",\s*([:;])\s*", r"\1 ", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    # le français veut une espace AVANT : ; ! ?
    t = re.sub(r"(?<=[^\s])([:;!?])(?=\s|$)", r" \1", t)
    return _rend(t).strip()
