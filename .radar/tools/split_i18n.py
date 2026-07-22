#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
split_i18n.py — CHANTIER PERF « différer les langues non affichées ».

Ce que fait l'outil, à partir d'un index.html COMPLET (source de vérité) :
  1. produit un index.html ALLÉGÉ : le bloc data ne garde que le français
     (champ `tr` retiré de chaque fiche) + un chargeur JS qui va chercher
     la langue demandée à la demande ;
  2. produit `i18n-data/<lang>.json` : un dictionnaire indexé par CLÉ STABLE
     « d1|nom » (et non par position : ajouter ou retirer un événement ne
     décale donc jamais les traductions) ;
  3. produit `index-full.html` : copie intégrale de la source, servie à
     l'artifact Claude (page autonome, aucun fetch possible → doit rester
     complète pour ne pas perdre les 12 langues).

Sécurité : l'outil N'ÉCRIT RIEN dans le dépôt tant que --apply n'est pas
passé. Par défaut il travaille dans un dossier d'essai (--out) pour qu'on
puisse mesurer et vérifier en local avant toute publication.

Usage :
  python3 split_i18n.py                       # essai dans /tmp/.../split-essai
  python3 split_i18n.py --out /chemin/essai
  python3 split_i18n.py --apply               # écrit dans le dépôt (après vérif)
"""
import argparse, json, os, re, shutil, sys, gzip

REPO = os.environ.get("RADAR_REPO", "/Users/geraldlefebvre/luxe-ete-2026")
SRC = os.path.join(REPO, "index.html")
DEFAULT_OUT = os.environ.get("RADAR_TMP", "/tmp") + "/split-essai"
LANGS = ["en", "es", "it", "pt", "de", "ru", "ar", "zh", "ja", "ko", "hi", "tr"]

DATA_RE = re.compile(r'(<script type="application/json" id="data">)(.*?)(</script>)', re.S)

# Chargeur injecté juste après la lecture de DATA dans le script applicatif.
LOADER = r"""
  /* ── traductions différées (perf mobile) ────────────────────────────────
     Le HTML n'embarque que le français ; chaque langue est un petit fichier
     chargé à la demande. Si le chargement échoue, l'affichage retombe sur le
     français : aucune page vide, aucun contenu perdu. ------------------- */
  const I18N_LOADED = {fr: true};
  // Clé stable (date de début + nom) : l'appariement ne dépend PAS de l'ordre
  // des fiches, donc ajouter ou retirer un événement ne décale rien.
  function i18nKey(e){ return (e.d1 || '') + '|' + (e.n || ''); }
  function loadLangData(lang){
    if (lang === 'fr' || I18N_LOADED[lang]) return Promise.resolve(true);
    return fetch('i18n-data/' + lang + '.json', {cache: 'force-cache'})
      .then(function(r){ if (!r.ok) throw new Error('http'); return r.json(); })
      .then(function(map){
        if (!map || typeof map !== 'object' || Array.isArray(map)) throw new Error('shape');
        for (var i = 0; i < DATA.length; i++){
          var t = map[i18nKey(DATA[i])];
          if (t) { (DATA[i].tr || (DATA[i].tr = {}))[lang] = t; }
        }
        I18N_LOADED[lang] = true;
        return true;
      })
      .catch(function(){ return false; });
  }
"""


def key_of(e):
    """Clé d'appariement d'une fiche avec sa traduction : indépendante de
    l'ordre du tableau, donc stable quand des événements sont ajoutés."""
    return f"{e.get('d1', '')}|{e.get('n', '')}"


def read_source(path):
    html = open(path, encoding="utf-8").read()
    m = DATA_RE.search(html)
    if not m:
        sys.exit("split_i18n: bloc data introuvable")
    data = json.loads(m.group(2).replace("<\\/", "</"))
    return html, m, data


def dump_data(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def build(out_dir, src=SRC):
    html, m, data = read_source(src)
    os.makedirs(os.path.join(out_dir, "i18n-data"), exist_ok=True)

    # 1) fichiers de langue, indexés par CLÉ STABLE (d1|nom) et non par
    #    position : ajouter ou retirer un événement ne décale plus rien.
    counts = {}
    for lang in LANGS:
        m2 = {}
        for e in data:
            t = (e.get("tr") or {}).get(lang)
            if t:
                m2[key_of(e)] = t
        counts[lang] = len(m2)
        p = os.path.join(out_dir, "i18n-data", lang + ".json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(m2, f, ensure_ascii=False, separators=(",", ":"))

    # 2) index.html allégé
    light = [{k: v for k, v in e.items() if k != "tr"} for e in data]
    new_html = html[:m.start(2)] + dump_data(light) + html[m.end(2):]
    anchor = "const DATA = JSON.parse(document.getElementById('data').textContent);"
    if anchor not in new_html:
        sys.exit("split_i18n: ancre DATA introuvable — script applicatif modifié ?")
    new_html = new_html.replace(anchor, anchor + "\n" + LOADER, 1)

    # setLang devient asynchrone (attend la langue avant de rendre)
    old_set = "  function setLang(lang){\n    if (!I18N[lang]) return;\n    LANG = lang;"
    new_set = ("  function setLang(lang){\n    if (!I18N[lang]) return;\n"
               "    loadLangData(lang).then(function(){ applyLang(lang); });\n  }\n"
               "  function applyLang(lang){\n    LANG = lang;")
    if old_set not in new_html:
        sys.exit("split_i18n: ancre setLang introuvable — script applicatif modifié ?")
    new_html = new_html.replace(old_set, new_set, 1)

    # au démarrage : si une langue est mémorisée, on la charge puis on re-rend
    boot_anchor = "  applyStaticI18n();\n  renderAll();"
    if boot_anchor not in new_html:
        sys.exit("split_i18n: ancre de démarrage introuvable")
    boot = ("  if (LANG !== 'fr') { loadLangData(LANG).then(function(ok){ if (ok) { renderAll(); renderIntl(); renderEntrees(); } }); }\n"
            + boot_anchor)
    new_html = new_html.replace(boot_anchor, boot, 1)

    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(new_html)

    # 3) version complète (artifact autonome)
    shutil.copyfile(src, os.path.join(out_dir, "index-full.html"))

    gz = lambda b: len(gzip.compress(b.encode("utf-8"), 6))
    print("=== split_i18n ===")
    print("événements            :", len(data))
    print("source (gzip)         : %.2f Mo" % (gz(html) / 1e6))
    print("index allégé (gzip)   : %.2f Mo" % (gz(new_html) / 1e6))
    for lang in LANGS:
        p = os.path.join(out_dir, "i18n-data", lang + ".json")
        print("  %s : %4d fiches, %5.0f Ko gzip" % (
            lang, counts[lang], gz(open(p, encoding="utf-8").read()) / 1e3))
    print("sortie                :", out_dir)
    return new_html, counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--apply", action="store_true", help="écrit dans le dépôt public")
    a = ap.parse_args()
    out = REPO if a.apply else a.out
    if a.apply:
        print("⚠️  écriture DANS LE DÉPÔT :", REPO)
    os.makedirs(out, exist_ok=True)
    build(out)


if __name__ == "__main__":
    main()
