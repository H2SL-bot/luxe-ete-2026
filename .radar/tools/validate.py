#!/usr/bin/env python3
"""validate.py — filet de sécurité du radar ConstanceParis7 (French Luxury Events).

À lancer AVANT chaque `git push` (étape 8 de la PROCÉDURE). Le script échoue
(code de sortie 1) dès qu'un BLOCKER est détecté : dans ce cas, NE PAS pousser.
Les WARN n'empêchent pas la publication mais doivent figurer au compte rendu.

Usage :
    python3 validate.py [chemin/vers/index.html]

Contrôles BLOCKER (font échouer le build) :
  - chaque bloc JSON (data, i18n, ld+json) reparse ;
  - le script applicatif passe `node --check` ;
  - chaque `dc` appartient à la liste autorisée (enum) ;
  - chaque contact `iv.c` a la forme {t, v} ;
  - chaque fiche affichée (c != 'acces') a des scores sv/sp/sl dans [0..100] ;
  - aucune fiche zombie (d2 < aujourd'hui - 30 j) restée non purgée.

Contrôles WARN (signalés, non bloquants) :
  - chute du compte > 10 % vs le dernier build (purge légitime possible) ;
  - fiches de la fenêtre live sans traduction `tr`.

Le script imprime aussi des KPIs, dont la COUVERTURE ACCÈS (iv) sur les fiches
mondaines — le cœur de valeur du site, à faire monter passe après passe.
"""
import re
import os
import sys
import json
import shutil
import tempfile
import subprocess
from datetime import date, timedelta, datetime

DEFAULT_PATH = os.environ.get("RADAR_REPO", "/Users/geraldlefebvre/luxe-ete-2026") + "/index.html"

DC_ENUM = {
    "Tenue de soirée / robe longue",
    "Chic décontracté (chapeau conseillé)",
    "Tenue blanche exigée",
    "Élégance estivale (chapeau bienvenu)",
    "Black tie (tenue de soirée)",
    "Tenue stricte (veste-cravate)",
    "Chic estival (panama, chapeau)",
}
LANGS = ["en", "es", "it", "pt", "de", "ru", "ar", "zh", "ja", "ko"]
MONDAIN_CATS = {"festival", "joaillerie", "art", "mode"}
# Mots-clés « mondain » : galas/soirées/défilés + sport très mondain (polo, voile,
# régate) et concours d'élégance — tous des événements où « apporter l'accès » (iv)
# fait la valeur du site. Élargi le 17/07/2026 pour que le KPI reflète le vrai périmètre.
MONDAIN_KW = ("gala", "soirée", "soiree", "défilé", "defile", "bal ",
              "polo", "voile", "régate", "regate", "concours", "élégance", "elegance")

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".last-count")
NAMES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".last-names.json")

# Champs lus par l'internaute, et résidus de fabrication qui n'ont rien à y faire :
# noms de champs du modèle (cf=, sv=, d1=…), valeurs Python/JS nues, balises de note.
HH_STRICT = ("ru", "ar", "hi", "tr")  # langues où « 20:00 » est la règle du SKILL

TEXT_FIELDS = ("n", "dt", "ds", "sw", "p", "pe", "ci", "ht", "l", "g", "v")
TECH_LEAK = re.compile(
    r"""\b(?:cf|sv|sp|sl|d1|d2|ct|dc|iv|so|pe|ci)\s*=|"""
    r"""\b(?:None|undefined|NaN)\b|\[object |TODO|FIXME|<script""",
)

blockers = []
warns = []


def blk(msg):
    blockers.append(msg)


def wrn(msg):
    warns.append(msg)


def tr_key(e):
    """Clé d'appariement fiche <-> traduction différée (voir split_i18n.py)."""
    return f"{e.get('d1', '')}|{e.get('n', '')}"


def parse_d(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    try:
        html = open(path, encoding="utf-8").read()
    except Exception as e:
        print(f"BLOCK  fichier illisible: {e}")
        sys.exit(1)

    # --- 1. Blocs JSON : présence + reparse ---
    blocks = {
        "data": r'<script type="application/json" id="data">(.*?)</script>',
        "i18n": r'<script type="application/json" id="i18n">(.*?)</script>',
        "ld+json": r'<script type="application/ld\+json">(.*?)</script>',
    }
    parsed = {}
    for name, pat in blocks.items():
        m = re.search(pat, html, re.S)
        if not m:
            blk(f"bloc JSON '{name}' introuvable")
            continue
        try:
            parsed[name] = json.loads(m.group(1))
        except Exception as e:
            blk(f"bloc JSON '{name}' ne reparse pas: {e}")
    data = parsed.get("data", []) or []

    # --- 1bis. Traductions différées (chantier perf) ---------------------
    # Si le dossier i18n-data/ existe à côté de la page, les traductions ne
    # sont plus dans le bloc data mais dans un fichier par langue, indexé par
    # clé stable « d1|nom ». On les recolle en mémoire pour que tous les
    # contrôles ci-dessous restent exacts, et on bloque si un fichier ne
    # correspond plus à aucune fiche (renommage en masse, mauvais format).
    i18n_dir = os.path.join(os.path.dirname(os.path.abspath(path)), "i18n-data")
    if os.path.isdir(i18n_dir):
        keys = {tr_key(e): e for e in data}
        for fn in sorted(os.listdir(i18n_dir)):
            if not fn.endswith(".json"):
                continue
            lang = fn[:-5]
            try:
                mp = json.load(open(os.path.join(i18n_dir, fn), encoding="utf-8"))
            except Exception as e:
                blk(f"i18n-data/{fn} ne reparse pas: {e}")
                continue
            if not isinstance(mp, dict) or not mp:
                blk(f"i18n-data/{fn} n'est pas un dictionnaire clé→traduction")
                continue
            hit = 0
            for k, t in mp.items():
                e = keys.get(k)
                if e is not None and t:
                    e.setdefault("tr", {})[lang] = t
                    hit += 1
            if hit < len(mp) * 0.5:
                blk(f"i18n-data/{fn} ne s'apparie plus qu'à {hit}/{len(mp)} fiches "
                    f"— clés désynchronisées, traductions perdues à l'affichage")

    # --- 2. node --check sur le(s) script(s) applicatif(s) inline ---
    scripts = re.findall(r"<script([^>]*)>(.*?)</script>", html, re.S)
    app = [
        body
        for attrs, body in scripts
        if "application/json" not in attrs
        and "application/ld+json" not in attrs
        and "src=" not in attrs
        and body.strip()
    ]
    node = shutil.which("node")
    if not node:
        wrn("node introuvable — contrôle syntaxe JS sauté")
    else:
        for i, body in enumerate(app):
            tmp = None
            try:
                with tempfile.NamedTemporaryFile(
                    "w", suffix=".js", delete=False, encoding="utf-8"
                ) as f:
                    f.write(body)
                    tmp = f.name
                r = subprocess.run(
                    [node, "--check", tmp], capture_output=True, text=True
                )
                if r.returncode != 0:
                    last = (r.stderr.strip().splitlines() or ["?"])[-1]
                    blk(f"node --check échoue sur script inline #{i}: {last}")
            finally:
                if tmp and os.path.exists(tmp):
                    os.unlink(tmp)

    # --- 3. Contrôles de schéma au niveau des fiches ---
    today = date.today()
    if not data:
        blk("bloc 'data' vide ou absent — aucun événement à valider")
    for e in data:
        n = (e.get("n") or "?")[:45]

        dc = e.get("dc")
        if dc not in (None, "") and dc not in DC_ENUM:
            blk(f"dc hors liste ({dc!r}) — {n}")

        iv = e.get("iv")
        if isinstance(iv, dict):
            for ct in iv.get("c", []) or []:
                if not (isinstance(ct, dict) and "t" in ct and "v" in ct):
                    blk(f"iv.c malformé (attendu {{t,v}}) — {n}")

        if e.get("c") != "acces":
            for k in ("sv", "sp", "sl"):
                v = e.get(k)
                if not isinstance(v, (int, float)) or isinstance(v, bool) or not (0 <= v <= 100):
                    blk(f"score {k} manquant/invalide ({v!r}) — {n}")
                    break

        d2 = parse_d(e.get("d2", "") or "")
        if d2 and d2 < today - timedelta(days=30):
            blk(f"zombie non purgé (d2={e.get('d2')}) — {n}")

        # Fuite de vocabulaire technique dans un texte lu par l'internaute
        # (ex. « …dates variables, cf='probable' » resté dans un champ dt).
        # Une fois traduit dans 12 langues, ce genre de résidu se démultiplie.
        for k in TEXT_FIELDS:
            v = e.get(k)
            if isinstance(v, str) and TECH_LEAK.search(v):
                blk(f"jargon technique visible dans '{k}' — {n}")

    # --- 4. Chute de compte vs baseline ---
    cnt = len(data)
    prev = None
    if os.path.exists(STATE_FILE):
        try:
            prev = int(open(STATE_FILE).read().strip())
        except Exception:
            prev = None
    if prev and cnt < prev * 0.9:
        wrn(f"compte en baisse: {prev} -> {cnt} (>10%) — confirmer qu'une purge le justifie")

    # --- 4bis. DISPARITIONS NON EXPLIQUÉES (BLOCKER) ---
    # Une fiche du build précédent qui n'est PAS périmée (d2 >= aujourd'hui-30j)
    # ne doit jamais disparaître : c'est une perte de données, pas une purge.
    # (Régression réelle du 21/07/2026 : 15 soirées vague 2 effacées par une
    #  régénération du bloc data depuis un instantané périmé.)
    cur_names = {e.get("n") for e in data if e.get("n")}
    prev_names = {}
    if os.path.exists(NAMES_FILE):
        try:
            prev_names = json.load(open(NAMES_FILE, encoding="utf-8"))
        except Exception:
            prev_names = {}
    disparues = []
    for nm, d2s in prev_names.items():
        if nm in cur_names:
            continue
        d2v = parse_d(d2s or "")
        if d2v is None or d2v >= today - timedelta(days=30):
            disparues.append((nm, d2s))
    if disparues:
        blk(f"{len(disparues)} fiche(s) NON PÉRIMÉE(S) ont disparu depuis le dernier build — perte de données probable :")
        for nm, d2s in disparues[:15]:
            blk(f"    disparue (d2={d2s}) — {nm[:60]}")
        blk("    -> restaurer depuis le dernier commit sain avant de pousser (git show <sha>:index.html)")

    # --- 4bis. Qualité des traductions (fautes récurrentes documentées) ---
    # Non bloquant : on signale pour retraduction ciblée, on ne retient pas la
    # publication — une fiche imparfaitement traduite vaut mieux qu'un site figé.
    esper = tr_hh = 0
    for e in data:
        for lang, t in (e.get("tr") or {}).items():
            for k, v in (t or {}).items():
                if not isinstance(v, str):
                    continue
                if "&amp;" in v:
                    esper += 1
                # Horaire à la française (« 20h », « 20h30 ») laissé tel quel.
                # Contrôle limité aux langues où le SKILL impose « 20:00 » :
                # en portugais ou en allemand, « 10h30 » / « 20 Uhr » sont
                # idiomatiques — alerter là-dessus serait du bruit.
                if lang in HH_STRICT and re.search(r"\b\d{1,2}\s?h(?:\d{2})?\b", v):
                    tr_hh += 1
    if esper:
        wrn(f"{esper} champ(s) traduits contiennent « &amp; » — l'esperluette ne doit jamais être échappée")
    if tr_hh:
        wrn(f"{tr_hh} champ(s) traduits gardent un horaire à la française (20h / 20h30) au lieu de 20:00")

    # --- 5. KPIs ---
    def d1_of(e):
        return parse_d(e.get("d1", "") or "")

    def is_mondain(e):
        if e.get("c") in MONDAIN_CATS:
            return True
        nm = (e.get("n") or "").lower()
        return any(k in nm for k in MONDAIN_KW)

    def has_access(e):
        iv = e.get("iv")
        return isinstance(iv, dict) and bool(iv.get("o") or iv.get("g") or iv.get("c"))

    window = [e for e in data if (d1_of(e) and today <= d1_of(e) <= today + timedelta(days=90))]
    past = sum(1 for e in data if (parse_d(e.get("d2", "") or "") or today) < today)
    beyond = sum(1 for e in data if (d1_of(e) or today) > today + timedelta(days=90))
    no_link = sum(1 for e in data if not e.get("u"))
    mond = [e for e in data if is_mondain(e)]
    mond_acc = sum(1 for e in mond if has_access(e))
    no_tr_window = [e for e in window if not e.get("tr")]
    no_tr_total = sum(1 for e in data if not e.get("tr"))

    if no_tr_window:
        wrn(f"{len(no_tr_window)} fiche(s) de la fenêtre live sans traduction tr — à combler (backlog)")

    # --- 6. Rappel de rafraîchissement de saison (WARN non bloquant) ---
    # Détecte le libellé de saison affiché dans la brandline (« French Luxury
    # Events · Été 2026 ») et suggère la bascule quand la saison touche à sa fin.
    # La fenêtre de préparation s'ouvre ~1 mois avant (esprit « vers le 25 août »).
    mlab = re.search(r'brandline[^>]*>.*?(Printemps|Été|Automne|Hiver)\s*\d{4}', html, re.S)
    cur_season = mlab.group(1) if mlab else None
    md = (today.month, today.day)

    def next_season(lbl):
        if lbl == "Été" and (8, 25) <= md and today.month <= 11:
            return "Automne"
        if lbl == "Automne" and (md >= (11, 25) or today.month == 12):
            return "Hiver"
        if lbl == "Hiver" and (2, 25) <= md and today.month <= 5:
            return "Printemps"
        if lbl == "Printemps" and (5, 25) <= md and today.month <= 8:
            return "Été"
        return None

    if cur_season:
        nxt = next_season(cur_season)
        if nxt:
            wrn(f"branding de saison : « {cur_season} » encore affiché au {today.isoformat()} — "
                f"proposer à Gérald le rafraîchissement « {nxt} » (ne jamais renommer sans son accord)")

    pct = lambda a, b: (100 * a // b) if b else 0
    print(f"=== validate.py — {path} ===")
    print(f"événements            : {cnt}")
    print(f"fenêtre [today..+90j] : {len(window)} | déjà passés: {past} | au-delà +90j: {beyond} | sans lien u: {no_link}")
    print(f"KPI ACCÈS mondain (iv): {mond_acc}/{len(mond)} ({pct(mond_acc, len(mond))}%)   <- cœur de valeur")
    print(f"traductions présentes : {cnt - no_tr_total}/{cnt} ({pct(cnt - no_tr_total, cnt)}%)")

    for w in warns:
        print("WARN  ", w)
    for b in blockers:
        print("BLOCK ", b)

    if not blockers:
        try:
            open(STATE_FILE, "w").write(str(cnt))
        except Exception:
            pass
        try:
            snap = {e["n"]: e.get("d2", "") for e in data if e.get("n")}
            json.dump(snap, open(NAMES_FILE, "w", encoding="utf-8"), ensure_ascii=False)
        except Exception:
            pass

    print(f"\n{'FAIL' if blockers else 'OK'} — {len(blockers)} blocker(s), {len(warns)} warning(s)")
    sys.exit(1 if blockers else 0)


if __name__ == "__main__":
    main()
