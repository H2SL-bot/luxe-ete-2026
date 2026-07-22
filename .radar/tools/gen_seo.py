#!/usr/bin/env python3
"""gen_seo.py — socle SEO du radar, 100% invisible pour l'internaute.

Fait DEUX choses, purement additives (n'altère jamais le rendu ni le contenu vu) :
  1. ENRICHIT le bloc ld+json (JSON-LD Event, dans le <head>) : ajoute à chaque
     événement, sans toucher aux champs existants, les 3 champs SEO manquants
     dérivés de VRAIES données du bloc data :
        - eventStatus      = EventScheduled (on purge les annulés)
        - organizer        = Organization {name, url} tiré du 1er segment propre
                             de iv.o + URL officielle de l'événement (e.u)
        - isAccessibleForFree = true si a == 'public', sinon false
        - offers           = Offer {url, availability} + price/priceCurrency
                             UNIQUEMENT si un prix réel est publié dans e.p
                             (parse conservateur ; jamais de prix inventé).
                             validFrom/performer : volontairement ABSENTS
                             (les renseigner serait fabriquer une donnée).
     (Réponse au signalement Search Console du 21/07/2026 — champs recommandés.)
  2. Régénère sitemap.xml avec un <lastmod> FRAIS (signal de fraîcheur pour Google).

Idempotent : relançable sans effet de bord. robots.txt (déjà correct) n'est pas
touché. Le JSON-LD est dans le <head> → aucun impact sur l'expérience utilisateur.

Usage : python3 gen_seo.py [AAAA-MM-JJ]   (date du lastmod ; défaut : aujourd'hui)
"""
import re, sys, json
from datetime import date

import os
REPO = os.environ.get("RADAR_REPO", "/Users/geraldlefebvre/luxe-ete-2026")
IDX = f"{REPO}/index.html"
SITEMAP = f"{REPO}/sitemap.xml"
HOME = "https://constanceparis7.com/"

lastmod = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()

html = open(IDX, encoding="utf-8").read()

# --- data : lookup nom -> {organizer, isFree} ---
md = re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S)
data = json.loads(md.group(1).replace("<\\/", "</"))

def org_name(iv):
    """1er segment propre de iv.o comme nom d'organisateur (sinon None)."""
    if not (isinstance(iv, dict) and iv.get("o")):
        return None
    seg = re.split(r"[,—(;]| - ", iv["o"].strip())[0].strip()
    return seg if 2 < len(seg) <= 80 else None

# Parse conservateur d'un prix RÉELLEMENT publié dans e.p (texte billetterie).
# Retourne (prix_min, devise) ou None. Jamais d'invention : sans symbole
# monétaire explicite, on ne retourne rien. (Dupliqué dans gen_pages.py.)
_CUR = {"€": "EUR", "EUR": "EUR", "$": "USD", "USD": "USD", "£": "GBP", "GBP": "GBP", "CHF": "CHF"}
_EU_Z = {"paris", "sainttropez", "cotedazur", "province"}

def _num(s):
    s = re.sub(r"[\s  ]", "", s)
    if re.fullmatch(r"\d+,\d{2}", s):
        s = s.replace(",", ".")
    else:
        s = s.replace(",", "")
    s = re.sub(r"\.(\d{3})(?!\d)", r"\1", s)
    try:
        return float(s)
    except ValueError:
        return None

def parse_price(e):
    p = e.get("p") or ""
    best = None
    for m in re.finditer(r"(\d(?:[\d\s  .,]{0,9}\d)?)\s?(€|EUR|\$|USD|£|GBP)", p):
        v = _num(m.group(1))
        if v is not None and v > 0 and (best is None or v < best[0]):
            best = (v, _CUR[m.group(2)])
    for m in re.finditer(r"(?:CHF)\s?(\d(?:[\d\s  .,]{0,9}\d)?)", p):
        v = _num(m.group(1))
        if v is not None and v > 0 and (best is None or v < best[0]):
            best = (v, "CHF")
    if best:
        return (int(best[0]) if best[0] == int(best[0]) else best[0]), best[1]
    if e.get("a") == "public" and e.get("z") in _EU_Z and \
       re.search(r"gratuit|entr[ée]e libre|libre et gratuite|acc[èe]s libre", p, re.I):
        return 0, "EUR"
    return None

lookup = {}
for e in data:
    lookup[(e.get("n") or "").strip()] = {
        "org": org_name(e.get("iv")),
        "free": (e.get("a") == "public"),
        "u": e.get("u"),
        "price": parse_price(e),
        "matched": True,
    }

# --- ld+json : enrichissement additif ---
ml = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', html, re.S)
ld = json.loads(ml.group(2))
graph = ld.get("@graph", [])
n_status = n_org = n_free = n_orgurl = n_offers = n_price = 0
for ev in graph:
    if ev.get("@type") != "Event":
        continue
    ev.setdefault("eventStatus", "https://schema.org/EventScheduled")
    n_status += 1
    info = lookup.get((ev.get("name") or "").strip())
    if info:
        if info["org"] and "organizer" not in ev:
            ev["organizer"] = {"@type": "Organization", "name": info["org"]}
            n_org += 1
        if isinstance(ev.get("organizer"), dict) and "url" not in ev["organizer"]:
            ou = info["u"] or ev.get("url")
            if ou and ou.startswith("http"):
                ev["organizer"]["url"] = ou
                n_orgurl += 1
        if "isAccessibleForFree" not in ev:
            ev["isAccessibleForFree"] = bool(info["free"])
            n_free += 1
        if "offers" not in ev:
            ou = info["u"] or ev.get("url") or HOME
            offer = {"@type": "Offer", "url": ou,
                     "availability": "https://schema.org/InStock"}
            if info["price"] is not None:
                offer["price"], offer["priceCurrency"] = info["price"]
                n_price += 1
            ev["offers"] = offer
            n_offers += 1

new_ld = json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html2 = html[:ml.start()] + ml.group(1) + new_ld + ml.group(3) + html[ml.end():]
open(IDX, "w", encoding="utf-8").write(html2)

# --- sitemap.xml avec lastmod frais ---
sitemap = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f'  <url><loc>{HOME}</loc><lastmod>{lastmod}</lastmod>'
    '<changefreq>daily</changefreq><priority>1.0</priority></url>\n'
    '</urlset>\n'
)
open(SITEMAP, "w", encoding="utf-8").write(sitemap)

print(f"gen_seo: ld+json enrichi — eventStatus:{n_status}  organizer:+{n_org}  organizer.url:+{n_orgurl}  isAccessibleForFree:+{n_free}  offers:+{n_offers} (dont prix réels:{n_price})")
print(f"gen_seo: sitemap.xml régénéré (lastmod={lastmod})")
