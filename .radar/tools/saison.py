#!/usr/bin/env python3
"""Met la SAISON du titre et du bandeau à jour, toute seule, au bon jour.

Demande de Gérald, 12/08/2026 : « Tu penses à changer Summer 2026 en Automne 2026
quand on passe de l'été à l'automne officiellement, et […] au jour approprié de passer
d'Automne 2026 à Winter 2026, le jour de l'hiver ? Pareil de Winter 2026 à Spring 2027
[…] en tête d'affiche pour Google. »

Le titre est ce que Google indexe : laissé à la main, il afficherait « Summer » en
décembre. Ce script est donc appelé à chaque passe automatique et bascule de lui-même
aux VRAIES dates astronomiques — équinoxes et solstices ne tombent pas le même jour
chaque année (22 ou 23 septembre, 21 ou 22 décembre, 20 ou 21 mars, 20 ou 21 juin).

Les instants sont calculés par l'algorithme de Jean Meeus (Astronomical Algorithms,
chap. 27), précis à la minute pour les siècles qui nous intéressent — plutôt qu'une
table en dur qui deviendrait fausse en silence le jour où on l'oublierait.

Le titre reste en ANGLAIS et unique : c'est une page servie en treize langues depuis
une seule URL, Google n'en indexe qu'un. Le bandeau affiché, lui, suit la langue du
visiteur et se traduit ici dans les treize.
"""
import datetime as dt
import json
import math
import os
import re
import sys

REPO = os.environ.get("RADAR_REPO") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Saison → libellé anglais du titre, puis libellé par langue pour le bandeau.
SAISONS = ("spring", "summer", "autumn", "winter")
ANGLAIS = {"spring": "Spring", "summer": "Summer", "autumn": "Autumn", "winter": "Winter"}
LIBELLES = {
    "fr": {"spring": "Printemps", "summer": "Été", "autumn": "Automne", "winter": "Hiver"},
    "en": {"spring": "Spring", "summer": "Summer", "autumn": "Autumn", "winter": "Winter"},
    "es": {"spring": "Primavera", "summer": "Verano", "autumn": "Otoño", "winter": "Invierno"},
    "it": {"spring": "Primavera", "summer": "Estate", "autumn": "Autunno", "winter": "Inverno"},
    "pt": {"spring": "Primavera", "summer": "Verão", "autumn": "Outono", "winter": "Inverno"},
    "de": {"spring": "Frühling", "summer": "Sommer", "autumn": "Herbst", "winter": "Winter"},
    "ru": {"spring": "Весна", "summer": "Лето", "autumn": "Осень", "winter": "Зима"},
    "ar": {"spring": "ربيع", "summer": "صيف", "autumn": "خريف", "winter": "شتاء"},
    "zh": {"spring": "春", "summer": "夏", "autumn": "秋", "winter": "冬"},
    "ja": {"spring": "春", "summer": "夏", "autumn": "秋", "winter": "冬"},
    "ko": {"spring": "봄", "summer": "여름", "autumn": "가을", "winter": "겨울"},
    "hi": {"spring": "वसंत", "summer": "ग्रीष्म", "autumn": "शरद", "winter": "शीत"},
    "tr": {"spring": "İlkbahar", "summer": "Yaz", "autumn": "Sonbahar", "winter": "Kış"},
}
# Ordre du libellé : « 2026年夏 » et « 2026 Yazı » se disent année d'abord.
ANNEE_DABORD = {"zh", "ja", "tr"}


def _jde(annee, k):
    """Instant (jour julien) de l'équinoxe/solstice. Meeus, chap. 27, 1000-3000."""
    y = (annee - 2000) / 1000.0
    base = {
        0: 2451623.80984 + 365242.37404 * y + 0.05169 * y**2 - 0.00411 * y**3 - 0.00057 * y**4,
        1: 2451716.56767 + 365241.62603 * y + 0.00325 * y**2 + 0.00888 * y**3 - 0.00030 * y**4,
        2: 2451810.21715 + 365242.01767 * y - 0.11575 * y**2 + 0.00337 * y**3 + 0.00078 * y**4,
        3: 2451900.05952 + 365242.74049 * y - 0.06223 * y**2 - 0.00823 * y**3 + 0.00032 * y**4,
    }[k]
    t = (base - 2451545.0) / 36525.0
    w = 35999.373 * t - 2.47
    lam = 1 + 0.0334 * math.cos(math.radians(w)) + 0.0007 * math.cos(math.radians(2 * w))
    termes = [
        (485, 324.96, 1934.136), (203, 337.23, 32964.467), (199, 342.08, 20.186),
        (182, 27.85, 445267.112), (156, 73.14, 45036.886), (136, 171.52, 22518.443),
        (77, 222.54, 65928.934), (74, 296.72, 3034.906), (70, 243.58, 9037.513),
        (58, 119.81, 33718.147), (52, 297.17, 150.678), (50, 21.02, 2281.226),
        (45, 247.54, 29929.562), (44, 325.15, 31555.956), (29, 60.93, 4443.417),
        (18, 155.12, 67555.328), (17, 288.79, 4562.452), (16, 198.04, 62894.029),
        (14, 199.76, 31436.921), (12, 95.39, 14577.848), (12, 287.11, 31931.756),
        (12, 320.81, 34777.259), (9, 227.73, 1222.114), (8, 15.45, 16859.074),
    ]
    s = sum(a * math.cos(math.radians(b + c * t)) for a, b, c in termes)
    return base + (0.00001 * s) / lam


def _date_utc(annee, k):
    jd = _jde(annee, k)
    # jour julien → date grégorienne
    z = int(jd + 0.5)
    f = (jd + 0.5) - z
    alpha = int((z - 1867216.25) / 36524.25)
    a = z + 1 + alpha - alpha // 4 if z >= 2299161 else z
    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    jour = b - d - int(30.6001 * e) + f
    mois = e - 1 if e < 14 else e - 13
    an = c - 4716 if mois > 2 else c - 4715
    return dt.datetime(an, mois, int(jour)) + dt.timedelta(days=jour - int(jour))


def saison_de(jour):
    """(saison, année d'affichage) pour une date donnée.

    Le millésime affiché est TOUJOURS l'année en cours, jamais celle de fin de saison.
    Gérald l'a formulé ainsi le 12/08/2026 : « d'Automne 2026 à Winter 2026, le jour de
    l'hiver ». Une première version affichait « Winter 2027 » dès le solstice de
    décembre 2026, au motif qu'on parle de la saison d'hiver par son millésime
    d'arrivée : c'est un usage défendable, mais ce n'est pas ce qui a été demandé, et
    un visiteur de décembre 2026 ne comprendrait pas de lire 2027.
    """
    a = jour.year
    bornes = [(_date_utc(a, k).date(), s) for k, s in
              zip((0, 1, 2, 3), ("spring", "summer", "autumn", "winter"))]
    if jour < bornes[0][0]:
        return "winter", a           # janvier-mars : hiver de l'année en cours
    for (d1, s1), (d2, _) in zip(bornes, bornes[1:]):
        if d1 <= jour < d2:
            return s1, a
    return "winter", a             # décembre : l'hiver porte l'année en cours


def appliquer(jour=None, ecrire=True):
    jour = jour or dt.date.today()
    saison, annee = saison_de(jour)
    F = os.path.join(REPO, "index-full.html")
    s = open(F, encoding="utf-8").read()

    attendu = f"{ANGLAIS[saison]} {annee}"
    # Le titre : une seule langue, l'anglais, parce que Google n'en indexe qu'un.
    motif = r"(ConstanceParis7 — International Luxury Events · )(Spring|Summer|Autumn|Winter) \d{4}"
    avant = re.search(motif, s)
    s2 = re.sub(motif, lambda m: m.group(1) + attendu, s)

    # Le bandeau : la langue du visiteur.
    m = re.search(r'(<script type="application/json" id="i18n">)(.*?)(</script>)', s2, re.S)
    i18n = json.loads(m.group(2))
    for lg, mots in LIBELLES.items():
        if lg not in i18n:
            continue
        # Demande de Constance, 21/08/2026 : la saison s'affiche EN ANGLAIS dans
        # toutes les langues — « Summer 2026 », jamais « Été 2026 » ni « 2026年夏 ».
        # C'est le choix cohérent : l'autre moitié du bandeau, « International
        # Luxury Events », n'est déjà traduite dans aucune langue. Le bandeau est
        # une signature de marque, pas une phrase à traduire.
        # LIBELLES et la particule d'année (zh/ja 年, ko 년, tr -ı) ne servent plus,
        # mais restent dans le fichier : le jour où l'on voudra retraduire, tout
        # est là, éprouvé.
        i18n[lg]["brandline_season"] = attendu
    s2 = s2[:m.start(2)] + json.dumps(i18n, ensure_ascii=False, separators=(",", ":")) + s2[m.end(2):]

    change = s2 != s
    if ecrire and change:
        open(F, "w", encoding="utf-8").write(s2)
    return saison, annee, attendu, (avant.group(2) + " " if avant else "?"), change


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    jour = dt.date.fromisoformat(args[0]) if args else None
    saison, annee, attendu, _, change = appliquer(jour, ecrire=("--dry" not in sys.argv))
    d = jour or dt.date.today()
    print(f"{d} → saison {saison} {annee} — titre « {attendu} »"
          + ("  (mis à jour)" if change else "  (déjà juste)"))
    if "--calendrier" in sys.argv:
        print("\nProchaines bascules :")
        vu = None
        for i in range(0, 800):
            j = dt.date.today() + dt.timedelta(days=i)
            s, a = saison_de(j)
            if vu and (s, a) != vu:
                print(f"   {j} → {ANGLAIS[s]} {a}")
            vu = (s, a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
