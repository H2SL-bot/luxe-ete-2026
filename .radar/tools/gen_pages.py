#!/usr/bin/env python3
"""gen_pages.py — pages statiques INDEXABLES, MULTILINGUES (11 langues), en AJOUT pur.

Le site visible est index.html : ce script NE LE MODIFIE JAMAIS. Il crée des
fichiers séparés, une arborescence par langue (FR à la racine, x-default) :
  - [<lang>/]e/<slug>.html    : page par événement (contenu traduit + accès + ld+json)
  - [<lang>/]lieu/<slug>.html : page par lieu
  - [<lang>/]type/<slug>.html : page par catégorie
  - [<lang>/]evenements.html  : hub
Chaque page porte les balises hreflang (11 alternates + x-default) et un canonical
propre. sitemap.xml liste la home + TOUTES les pages créées (jamais de 404).

Contenu traduit : pioché dans le champ tr[lang] des données (déjà présent). Libellés
de catégories : réutilisés du bloc i18n (déjà traduits). Micro-libellés d'interface :
dictionnaire UI ci-dessous. Aucune traduction inventée de contenu.

Sûreté : pages autonomes (polices système, aucun fetch externe → aucun risque réseau,
Chine incluse) ; arabe en dir=rtl. Idempotent. Publication ATOMIQUE et manuelle.

Usage : python3 gen_pages.py
"""
import re, os, json, html, unicodedata, shutil
from datetime import date

# --- Prix réel publié (parse conservateur ; dupliqué de gen_seo.py) -----------
# Réponse au signalement Search Console du 21/07/2026 : offers.price/priceCurrency
# et organizer.url quand la donnée est RÉELLE. Jamais de prix inventé ;
# validFrom/performer volontairement absents (les renseigner = fabriquer).
_CUR = {"€": "EUR", "EUR": "EUR", "$": "USD", "USD": "USD", "£": "GBP", "GBP": "GBP", "CHF": "CHF"}
_EU_Z = {"paris", "sainttropez", "cotedazur", "province"}

def _num(s):
    s = re.sub(r"[\s  ]", "", s)
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
    for m in re.finditer(r"(\d(?:[\d\s  .,]{0,9}\d)?)\s?(€|EUR|\$|USD|£|GBP)", p):
        v = _num(m.group(1))
        if v is not None and v > 0 and (best is None or v < best[0]):
            best = (v, _CUR[m.group(2)])
    for m in re.finditer(r"(?:CHF)\s?(\d(?:[\d\s  .,]{0,9}\d)?)", p):
        v = _num(m.group(1))
        if v is not None and v > 0 and (best is None or v < best[0]):
            best = (v, "CHF")
    if best:
        return (int(best[0]) if best[0] == int(best[0]) else best[0]), best[1]
    if e.get("a") == "public" and e.get("z") in _EU_Z and \
       re.search(r"gratuit|entr[ée]e libre|libre et gratuite|acc[èe]s libre", p, re.I):
        return 0, "EUR"
    return None

def org_name_from_iv(e):
    iv = e.get("iv")
    if not (isinstance(iv, dict) and iv.get("o")):
        return None
    seg = re.split(r"[,—(;]| - ", iv["o"].strip())[0].strip()
    return seg if 2 < len(seg) <= 80 else None

REPO = os.environ.get("RADAR_REPO", "/Users/geraldlefebvre/luxe-ete-2026")
IDX = f"{REPO}/index.html"
BASE = "https://constanceparis7.com"
OG = f"{BASE}/og-image.png"
TODAY = date.today().isoformat()

LANGS = ["fr", "en", "es", "it", "pt", "de", "ru", "ar", "zh", "ja", "ko"]
RTL = {"ar"}
CAT_I18N = {"art": "c_art", "mode": "c_mode", "artdevivre": "c_art2",
            "festival": "c_fest", "joaillerie": "c_joa", "sport": "c_sport", "autre": "c_other"}

# Micro-libellés d'interface (à relire par le workflow multilingue).
UI = {
 "radar":   {"fr":"Radar","en":"Radar","es":"Radar","it":"Radar","pt":"Radar","de":"Radar","ru":"Радар","ar":"الرادار","zh":"雷达","ja":"レーダー","ko":"레이더"},
 "all":     {"fr":"Tout","en":"All","es":"Todo","it":"Tutto","pt":"Tudo","de":"Alle","ru":"Все","ar":"الكل","zh":"全部","ja":"すべて","ko":"전체"},
 "affiche": {"fr":"À l'affiche","en":"Line-up","es":"En cartel","it":"In scena","pt":"Em cartaz","de":"Programm","ru":"В программе","ar":"المشاركون","zh":"阵容","ja":"出演","ko":"라인업"},
 "access":  {"fr":"Comment y accéder","en":"How to get in","es":"Cómo acceder","it":"Come accedere","pt":"Como aceder","de":"So kommen Sie hinein","ru":"Как попасть","ar":"كيفية الدخول","zh":"如何进入","ja":"アクセス方法","ko":"입장 방법"},
 "access2": {"fr":"Accès","en":"Access","es":"Acceso","it":"Accesso","pt":"Acesso","de":"Zugang","ru":"Доступ","ar":"الدخول","zh":"入场","ja":"アクセス","ko":"입장"},
 "official":{"fr":"Site officiel de l'événement","en":"Official event website","es":"Web oficial del evento","it":"Sito ufficiale dell'evento","pt":"Site oficial do evento","de":"Offizielle Website der Veranstaltung","ru":"Официальный сайт события","ar":"الموقع الرسمي للفعالية","zh":"活动官方网站","ja":"イベント公式サイト","ko":"이벤트 공식 사이트"},
 "all_in":  {"fr":"Tous les événements","en":"All events","es":"Todos los eventos","it":"Tutti gli eventi","pt":"Todos os eventos","de":"Alle Veranstaltungen","ru":"Все события","ar":"جميع الفعاليات","zh":"全部活动","ja":"すべてのイベント","ko":"모든 이벤트"},
 "back":    {"fr":"Retour au radar","en":"Back to the radar","es":"Volver al radar","it":"Torna al radar","pt":"Voltar ao radar","de":"Zurück zum Radar","ru":"Назад к радару","ar":"العودة إلى الرادار","zh":"返回雷达","ja":"レーダーに戻る","ko":"레이더로 돌아가기"},
 "places_cats":{"fr":"Tous les lieux & catégories","en":"All places & categories","es":"Todos los lugares y categorías","it":"Tutti i luoghi e le categorie","pt":"Todos os locais e categorias","de":"Alle Orte & Kategorien","ru":"Все места и категории","ar":"جميع الأماكن والفئات","zh":"所有地点与类别","ja":"すべての場所とカテゴリー","ko":"모든 장소 및 카테고리"},
 "events":  {"fr":"événements","en":"events","es":"eventos","it":"eventi","pt":"eventos","de":"Veranstaltungen","ru":"событий","ar":"فعاليات","zh":"项活动","ja":"件のイベント","ko":"개 이벤트"},
 "tagline": {"fr":"Sélection au niveau Riviera : dates, lieux et modes d'accès.","en":"A Riviera-level selection: dates, venues and how to get in.","es":"Una selección de nivel Riviera: fechas, lugares y cómo acceder.","it":"Una selezione di livello Riviera: date, luoghi e come accedere.","pt":"Uma seleção ao nível da Riviera: datas, locais e como aceder.","de":"Eine Auswahl auf Riviera-Niveau: Termine, Orte und Zugang.","ru":"Подборка уровня Ривьеры: даты, места и как попасть.","ar":"اختيار بمستوى الريفييرا: التواريخ والأماكن وكيفية الدخول.","zh":"蔚蓝海岸级别的精选：日期、地点与入场方式。","ja":"リヴィエラ級のセレクション：日程、会場、入場方法。","ko":"리비에라급 셀렉션: 날짜, 장소, 입장 방법."},
 "hub_h1":  {"fr":"Tous les événements du luxe","en":"All luxury events","es":"Todos los eventos de lujo","it":"Tutti gli eventi del lusso","pt":"Todos os eventos de luxo","de":"Alle Luxus-Veranstaltungen","ru":"Все события мира роскоши","ar":"جميع فعاليات الفخامة","zh":"全部奢华活动","ja":"すべてのラグジュアリー・イベント","ko":"모든 럭셔리 이벤트"},
 "hub_intro":{"fr":"Parcourez par lieu ou par catégorie. Le radar complet, en direct et en 11 langues, est sur ConstanceParis7.","en":"Browse by place or by category. The full radar, live and in 11 languages, is on ConstanceParis7.","es":"Explore por lugar o por categoría. El radar completo, en directo y en 11 idiomas, está en ConstanceParis7.","it":"Sfoglia per luogo o per categoria. Il radar completo, in diretta e in 11 lingue, è su ConstanceParis7.","pt":"Navegue por local ou por categoria. O radar completo, em direto e em 11 línguas, está no ConstanceParis7.","de":"Stöbern Sie nach Ort oder Kategorie. Das vollständige Radar, live und in 11 Sprachen, finden Sie auf ConstanceParis7.","ru":"Ищите по месту или категории. Полный радар — в реальном времени и на 11 языках — на ConstanceParis7.","ar":"تصفّح حسب المكان أو الفئة. الرادار الكامل، مباشرةً وبإحدى عشرة لغة، على ConstanceParis7.","zh":"按地点或类别浏览。完整雷达，实时更新、11 种语言，尽在 ConstanceParis7。","ja":"場所またはカテゴリーで探せます。完全版レーダー（ライブ・11言語）は ConstanceParis7 にて。","ko":"장소 또는 카테고리로 탐색하세요. 실시간 11개 언어의 전체 레이더는 ConstanceParis7에서."},
 "by_cat":  {"fr":"Par catégorie","en":"By category","es":"Por categoría","it":"Per categoria","pt":"Por categoria","de":"Nach Kategorie","ru":"По категориям","ar":"حسب الفئة","zh":"按类别","ja":"カテゴリー別","ko":"카테고리별"},
 "by_place":{"fr":"Par lieu","en":"By place","es":"Por lugar","it":"Per luogo","pt":"Por local","de":"Nach Ort","ru":"По местам","ar":"حسب المكان","zh":"按地点","ja":"場所別","ko":"장소별"},
 "footer":  {"fr":"ConstanceParis7 — le radar des événements du luxe, mis à jour chaque jour.","en":"ConstanceParis7 — the radar of luxury events, updated every day.","es":"ConstanceParis7 — el radar de los eventos de lujo, actualizado cada día.","it":"ConstanceParis7 — il radar degli eventi del lusso, aggiornato ogni giorno.","pt":"ConstanceParis7 — o radar dos eventos de luxo, atualizado todos os dias.","de":"ConstanceParis7 — das Radar der Luxus-Veranstaltungen, täglich aktualisiert.","ru":"ConstanceParis7 — радар событий мира роскоши, обновляется каждый день.","ar":"ConstanceParis7 — رادار فعاليات الفخامة، يُحدَّث كل يوم.","zh":"ConstanceParis7 — 奢华活动雷达，每日更新。","ja":"ConstanceParis7 — ラグジュアリー・イベントのレーダー。毎日更新。","ko":"ConstanceParis7 — 매일 업데이트되는 럭셔리 이벤트 레이더."},
 "see_live":{"fr":"Voir tout le radar en direct","en":"See the full radar live","es":"Ver todo el radar en directo","it":"Vedi tutto il radar in diretta","pt":"Ver todo o radar em direto","de":"Das ganze Radar live ansehen","ru":"Смотреть весь радар в реальном времени","ar":"شاهد الرادار الكامل مباشرةً","zh":"查看完整实时雷达","ja":"完全版レーダーをライブで見る","ko":"전체 레이더 실시간 보기"},
 "luxury_events":{"fr":"événements du luxe","en":"luxury events","es":"eventos de lujo","it":"eventi del lusso","pt":"eventos de luxo","de":"Luxus-Veranstaltungen","ru":"события роскоши","ar":"فعاليات الفخامة","zh":"奢华活动","ja":"ラグジュアリー・イベント","ko":"럭셔리 이벤트"},
}


def esc(x):
    return html.escape(str(x if x is not None else ""))


def slugify(s, maxlen=64):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s[:maxlen].strip("-") or "x"


def verifie_depot():
    """Ce script SUPPRIME des dossiers entiers sous REPO (voir la purge des
    sorties plus bas). Si RADAR_REPO désignait autre chose que le dépôt du site
    — erreur d'environnement, très possible en exécution distante — on effacerait
    le travail d'un autre dépôt. Deux preuves d'identité sont exigées avant tout."""
    if not os.path.isfile(IDX):
        raise SystemExit(f"gen_pages: {REPO} ne contient pas index.html — refus d'agir")
    import subprocess
    try:
        origin = subprocess.run(["git", "-C", REPO, "remote", "get-url", "origin"],
                                capture_output=True, text=True).stdout.strip()
    except Exception:
        origin = ""
    if origin and "luxe-ete-2026" not in origin:
        raise SystemExit(f"gen_pages: dépôt inattendu ({origin}) — refus d'agir")


def main():
    verifie_depot()
    src = open(IDX, encoding="utf-8").read()
    data = json.loads(re.search(r'<script type="application/json" id="data">(.*?)</script>', src, re.S).group(1).replace("<\\/", "</"))
    i18n = json.loads(re.search(r'<script type="application/json" id="i18n">(.*?)</script>', src, re.S).group(1))

    # Traductions différées (chantier perf) : quand elles ne sont plus dans le
    # bloc data mais dans i18n-data/<lang>.json, on les recolle avant de
    # générer — les pages statiques doivent rester traduites.
    i18n_dir = os.path.join(os.path.dirname(os.path.abspath(IDX)), "i18n-data")
    if os.path.isdir(i18n_dir):
        for fn in sorted(os.listdir(i18n_dir)):
            if not fn.endswith(".json"):
                continue
            try:
                arr = json.load(open(os.path.join(i18n_dir, fn), encoding="utf-8"))
            except Exception:
                continue
            if isinstance(arr, dict):
                keys = {f"{e.get('d1','')}|{e.get('n','')}": e for e in data}
                for k, t in arr.items():
                    e = keys.get(k)
                    if e is not None and t:
                        e.setdefault("tr", {})[fn[:-5]] = t

    pages = [e for e in data if e.get("c") != "acces"]

    # slugs (identiques pour toutes les langues ; l'URL diffère par le préfixe)
    seen = set()
    for e in pages:
        base = slugify(f"{e.get('n','')}-{e.get('v') or e.get('g') or ''}")
        slug, i = base, 2
        while slug in seen:
            slug = f"{base}-{i}"; i += 1
        seen.add(slug); e["_slug"] = slug

    places, pseen = {}, set()
    for e in pages:
        k = (e.get("g") or e.get("v") or "").strip()
        if not k:
            continue
        places.setdefault(k, {"events": []})["events"].append(e)
        e["_pk"] = k
    for k, v in places.items():
        base = slugify(k); slug, i = base, 2
        while slug in pseen:
            slug = f"{base}-{i}"; i += 1
        pseen.add(slug); v["slug"] = slug

    cats = {}
    for e in pages:
        c = e.get("c", "autre")
        cats.setdefault(c, {"slug": slugify(c), "events": []})["events"].append(e)

    def sort_key(e):
        return 0.4 * (e.get("sv") or 0) + 0.3 * (e.get("sp") or 0) + 0.2 * (e.get("sl") or 0)

    def T(e, lang, key):
        """champ traduit si dispo (lang != fr), sinon FR ; None si absent."""
        if lang != "fr":
            v = (e.get("tr") or {}).get(lang, {}).get(key)
            if v:
                return v
            if key in ("n", "dt", "ds", "sw"):  # champs universels → repli FR (jamais vide)
                return e.get(key)
            return None
        return e.get(key)

    def cat_label(c, lang):
        return i18n.get(lang, i18n["fr"]).get(CAT_I18N.get(c, "c_other"), c)

    def prefix(lang):
        return "" if lang == "fr" else f"/{lang}"

    def u_event(e, lang):
        return f"{prefix(lang)}/e/{e['_slug']}.html"

    def u_place(v, lang):
        return f"{prefix(lang)}/lieu/{v['slug']}.html"

    def u_cat(v, lang):
        return f"{prefix(lang)}/type/{v['slug']}.html"

    def u_hub(lang):
        return f"{prefix(lang)}/evenements.html"

    def hreflang_for(path_fn, obj):
        """balises alternate pour une entité, à travers les 11 langues + x-default."""
        out = []
        for L in LANGS:
            out.append(f'<link rel="alternate" hreflang="{L}" href="{BASE}{path_fn(obj, L) if obj is not None else u_hub(L)}">')
        out.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}{path_fn(obj, "fr") if obj is not None else u_hub("fr")}">')
        return "".join(out)

    def page(lang, title, desc, path, body, hreflang, ld=None):
        ldblock = ""
        if ld is not None:
            j = json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
            ldblock = f'<script type="application/ld+json">{j}</script>'
        dirattr = ' dir="rtl"' if lang in RTL else ""
        canonical = f"{BASE}{path}"
        return (
            f"<!doctype html><html lang=\"{lang}\"{dirattr}><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(title)}</title><meta name=\"description\" content=\"{esc(desc)}\">"
            f"<link rel=\"canonical\" href=\"{canonical}\">{hreflang}"
            "<meta property=\"og:type\" content=\"website\">"
            f"<meta property=\"og:title\" content=\"{esc(title)}\"><meta property=\"og:description\" content=\"{esc(desc)}\">"
            f"<meta property=\"og:url\" content=\"{canonical}\"><meta property=\"og:image\" content=\"{OG}\">"
            f"<style>{CSS}</style>{ldblock}</head><body><div class=\"wrap\">"
            f"<header class=\"site\"><a href=\"{prefix(lang)}/\" class=\"brand\">ConstanceParis<span class=\"s\">7</span></a>"
            "<div class=\"edition\">French Luxury Events</div></header>"
            f"{body}"
            f"<footer class=\"site\">{esc(UI['footer'][lang])} "
            f"<a href=\"/\">{esc(UI['see_live'][lang])} →</a></footer></div></body></html>"
        )

    # purge + recrée les sorties (jamais index.html)
    for lang in LANGS:
        for kind in ("e", "lieu", "type"):
            p = os.path.join(REPO, prefix(lang).lstrip("/"), kind) if lang != "fr" else os.path.join(REPO, kind)
            if os.path.isdir(p):
                shutil.rmtree(p)
            os.makedirs(p)

    def write(path, content):
        fp = REPO + path
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(content)

    sitemap_urls = [f"{BASE}/"]

    for lang in LANGS:
        # --- pages événement ---
        for e in pages:
            path = u_event(e, lang)
            pk = e.get("_pk"); lieu = places.get(pk) if pk else None
            cat = cats.get(e.get("c", "autre"))
            n = T(e, lang, "n"); ville = e.get("v") or (pk or "")
            title = f"{n} — {ville} | ConstanceParis7"
            desc = (T(e, lang, "sw") or T(e, lang, "ds") or "")[:155]
            bc = f"<div class=\"bc\"><a href=\"{prefix(lang)}/\">{esc(UI['radar'][lang])}</a>"
            if lieu:
                bc += f" › <a href=\"{u_place(lieu, lang)}\">{esc(pk)}</a>"
            bc += "</div>"
            body = [bc, f"<h1>{esc(n)}</h1>"]
            meta = []
            if T(e, lang, "dt"):
                meta.append(f"<b>{esc(T(e,lang,'dt'))}</b>")
            if e.get("l") or e.get("v"):
                meta.append(esc(e.get("l") or e.get("v")))
            if cat:
                meta.append(f"<a href=\"{u_cat(cat, lang)}\">{esc(cat_label(e.get('c','autre'), lang))}</a>")
            body.append("<div class=\"meta\">" + " · ".join(meta) + "</div>")
            if T(e, lang, "ds"):
                body.append(f"<p>{esc(T(e,lang,'ds'))}</p>")
            if T(e, lang, "pe"):
                body.append(f"<p><b>{esc(UI['affiche'][lang])} :</b> {esc(T(e,lang,'pe'))}</p>")
            # accès : privilégier iv traduit ; sinon p traduit ; jamais de FR résiduel sur non-FR
            ivo, ivw = T(e, lang, "iv_o"), T(e, lang, "iv_w")
            if ivo or ivw:
                acc = [f"<div class=\"box\"><h2>{esc(UI['access'][lang])}</h2>"]
                if ivo:
                    acc.append(f"<p>{esc(ivo)}</p>")
                if ivw:
                    acc.append(f"<p>{esc(ivw)}</p>")
                if lang == "fr":  # liste de contacts structurée : libellés FR → FR uniquement
                    cs = [c for c in ((e.get("iv") or {}).get("c") or []) if isinstance(c, dict) and c.get("t")]
                    if cs:
                        acc.append("<ul>" + "".join(f"<li><b>{esc(c['t'])} :</b> {esc(c.get('v'))}</li>" for c in cs) + "</ul>")
                acc.append("</div>")
                body.append("".join(acc))
            elif T(e, lang, "p"):
                body.append(f"<div class=\"box\"><h2>{esc(UI['access2'][lang])}</h2><p>{esc(T(e,lang,'p'))}</p></div>")
            if e.get("u"):
                body.append(f"<p><a class=\"cta\" href=\"{esc(e['u'])}\" target=\"_blank\" rel=\"noopener nofollow\">{esc(UI['official'][lang])} →</a></p>")
            nav = []
            if lieu:
                nav.append(f"<a href=\"{u_place(lieu, lang)}\">{esc(UI['all_in'][lang])} · {esc(pk)}</a>")
            if cat:
                nav.append(f"<a href=\"{u_cat(cat, lang)}\">{esc(cat_label(e.get('c','autre'), lang))}</a>")
            nav.append(f"<a href=\"{prefix(lang)}/\">← {esc(UI['back'][lang])}</a>")
            body.append("<div class=\"chips\">" + "".join(nav) + "</div>")

            ld = {"@context": "https://schema.org", "@type": "Event", "name": n,
                  "startDate": e.get("d1", ""), "endDate": e.get("d2", e.get("d1", "")),
                  "eventStatus": "https://schema.org/EventScheduled",
                  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                  "location": {"@type": "Place", "name": e.get("l") or e.get("v") or "",
                               "address": {"@type": "PostalAddress", "addressLocality": e.get("v") or pk or ""}},
                  "image": OG, "description": (T(e, lang, "ds") or T(e, lang, "sw") or "")[:300],
                  "url": f"{BASE}{path}", "inLanguage": lang, "isAccessibleForFree": (e.get("a") == "public")}
            offer = {"@type": "Offer", "url": e.get("u") or f"{BASE}{path}",
                     "availability": "https://schema.org/InStock"}
            pr = parse_price(e)
            if pr is not None:
                offer["price"], offer["priceCurrency"] = pr
            ld["offers"] = offer
            org = org_name_from_iv(e)
            if org:
                ld["organizer"] = {"@type": "Organization", "name": org}
                if e.get("u"):
                    ld["organizer"]["url"] = e["u"]
            hl = hreflang_for(u_event, e)
            write(path, page(lang, title, desc, path, "".join(body), hl, ld))
            sitemap_urls.append(f"{BASE}{path}")

        # --- pages lieu & catégorie ---
        def list_page(label, path, events, obj, path_fn):
            events = sorted(events, key=sort_key, reverse=True)
            title = f"{label} — {UI['luxury_events'][lang]} | ConstanceParis7"
            desc = f"{len(events)} {UI['events'][lang]} — {label}. {UI['tagline'][lang]}"
            body = [f"<div class=\"bc\"><a href=\"{prefix(lang)}/\">{esc(UI['radar'][lang])}</a> › "
                    f"<a href=\"{u_hub(lang)}\">{esc(UI['all'][lang])}</a></div>",
                    f"<h1>{esc(label)}</h1>",
                    f"<p class=\"meta\">{len(events)} {esc(UI['events'][lang])} — {esc(UI['tagline'][lang])}</p>",
                    "<ul class=\"cards\">"]
            for e in events:
                body.append(f"<li><div class=\"d\">{esc(T(e,lang,'dt') or e.get('d1',''))}</div>"
                            f"<a class=\"t\" href=\"{u_event(e, lang)}\">{esc(T(e,lang,'n'))}</a>"
                            + (f"<div>{esc((T(e,lang,'sw') or '')[:120])}</div>" if T(e, lang, "sw") else "") + "</li>")
            body.append(f"</ul><div class=\"chips\"><a href=\"{u_hub(lang)}\">{esc(UI['places_cats'][lang])}</a>"
                        f"<a href=\"{prefix(lang)}/\">← {esc(UI['back'][lang])}</a></div>")
            hl = hreflang_for(path_fn, obj)
            write(path, page(lang, title, desc, path, "".join(body), hl))
            sitemap_urls.append(f"{BASE}{path}")

        for k, v in places.items():
            list_page(k, u_place(v, lang), v["events"], v, u_place)
        for c, v in cats.items():
            list_page(cat_label(c, lang), u_cat(v, lang), v["events"], v, u_cat)

        # --- hub ---
        hub = [f"<div class=\"bc\"><a href=\"{prefix(lang)}/\">{esc(UI['radar'][lang])}</a></div>",
               f"<h1>{esc(UI['hub_h1'][lang])}</h1>",
               f"<p class=\"meta\">{esc(UI['hub_intro'][lang])}</p>",
               f"<h2 class=\"sub\">{esc(UI['by_cat'][lang])}</h2><div class=\"chips\">"]
        for c, v in sorted(cats.items(), key=lambda kv: -len(kv[1]["events"])):
            hub.append(f"<a href=\"{u_cat(v, lang)}\">{esc(cat_label(c, lang))} ({len(v['events'])})</a>")
        hub.append(f"</div><h2 class=\"sub\">{esc(UI['by_place'][lang])}</h2><div class=\"chips\">")
        for k, v in sorted(places.items(), key=lambda kv: -len(kv[1]["events"])):
            hub.append(f"<a href=\"{u_place(v, lang)}\">{esc(k)} ({len(v['events'])})</a>")
        hub.append("</div>")
        htitle = f"{UI['hub_h1'][lang]} | ConstanceParis7"
        write(u_hub(lang), page(lang, htitle, UI["hub_intro"][lang], u_hub(lang), "".join(hub), hreflang_for(None, None)))
        sitemap_urls.append(f"{BASE}{u_hub(lang)}")

    # --- sitemap ---
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sitemap_urls:
        pr = "1.0" if u == f"{BASE}/" else ("0.8" if ("/evenements" in u or "/lieu/" in u or "/type/" in u) else "0.6")
        cf = "daily" if u == f"{BASE}/" else "weekly"
        sm.append(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    open(f"{REPO}/sitemap.xml", "w", encoding="utf-8").write("\n".join(sm) + "\n")

    print(f"gen_pages: {len(pages)} événements × {len(LANGS)} langues + lieux/catégories/hub")
    print(f"gen_pages: sitemap.xml = {len(sitemap_urls)} URLs")
    print("gen_pages: index.html NON modifié (site visible intact).")


CSS = (
    "*{box-sizing:border-box}"
    "body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;"
    "background:#0e1317;color:#e9e6df;line-height:1.6;-webkit-text-size-adjust:100%}"
    "a{color:#e9c46a;text-decoration:none}a:hover{text-decoration:underline}"
    ".wrap{max-width:780px;margin:0 auto;padding:22px 18px 60px}"
    "header.site{border-bottom:1px solid #26313a;padding:14px 0;margin-bottom:8px}"
    ".brand{font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:15px;color:#fff}"
    ".brand .s{color:#e9c46a}"
    ".edition{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#9fb0bd}"
    ".bc{font-size:12px;letter-spacing:.05em;color:#9fb0bd;margin:14px 0}"
    "h1{font-size:1.7rem;line-height:1.25;margin:.2em 0 .3em;color:#fff;font-weight:700}"
    "h2.sub{color:#e9c46a;letter-spacing:.06em;text-transform:uppercase;font-size:1rem;margin:1.4em 0 .2em}"
    ".meta{color:#b9c6d1;font-size:.95rem;margin-bottom:1.2em}.meta b{color:#e9c46a;font-weight:600}"
    "p{margin:.7em 0}"
    ".box{background:#151d23;border:1px solid #26313a;border-radius:12px;padding:16px 18px;margin:18px 0}"
    ".box h2{font-size:1rem;letter-spacing:.06em;text-transform:uppercase;color:#e9c46a;margin:.1em 0 .6em}"
    ".box ul{margin:.4em 0;padding-left:1.1em}.box li{margin:.3em 0}"
    ".cta{display:inline-block;background:#e9c46a;color:#0e1317;font-weight:700;padding:11px 18px;border-radius:10px;margin:6px 0}"
    ".cta:hover{text-decoration:none;background:#f0d488}"
    ".cards{list-style:none;padding:0;margin:16px 0}.cards li{border-bottom:1px solid #26313a;padding:12px 0}"
    ".cards .d{color:#9fb0bd;font-size:.85rem;letter-spacing:.05em}.cards .t{font-size:1.05rem;color:#fff;font-weight:600}"
    ".chips{margin:16px 0}.chips a{display:inline-block;background:#151d23;border:1px solid #26313a;border-radius:20px;padding:6px 13px;margin:4px 4px 4px 0;font-size:.9rem}"
    "footer.site{border-top:1px solid #26313a;margin-top:34px;padding-top:16px;color:#8b9aa6;font-size:.85rem}"
    "[dir=rtl] .box ul{padding-left:0;padding-right:1.1em}[dir=rtl] .chips a{margin:4px 0 4px 4px}"
    "@media(max-width:520px){h1{font-size:1.4rem}.wrap{padding:16px 14px 48px}}"
)

if __name__ == "__main__":
    main()
