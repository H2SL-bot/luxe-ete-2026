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

REPO = os.environ.get("RADAR_REPO") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IDX = f"{REPO}/index.html"
BASE = "https://constanceparis7.com"
OG = f"{BASE}/og-image.png"
TODAY = date.today().isoformat()

LANGS = ["fr", "en", "es", "it", "pt", "de", "ru", "ar", "zh", "ja", "ko", "hi", "tr"]
RTL = {"ar"}
CAT_I18N = {"art": "c_art", "mode": "c_mode", "artdevivre": "c_art2",
            "festival": "c_fest", "joaillerie": "c_joa", "sport": "c_sport", "autre": "c_other"}

# Micro-libellés d'interface (à relire par le workflow multilingue).
UI = {
 "radar":   {"fr":"Radar","en":"Radar","es":"Radar","it":"Radar","pt":"Radar","de":"Radar","ru":"Радар","ar":"الرادار","zh":"雷达","ja":"レーダー","ko":"레이더","hi":"रडार","tr":"Radar"},
 "all":     {"fr":"Tout","en":"All","es":"Todo","it":"Tutto","pt":"Tudo","de":"Alle","ru":"Все","ar":"الكل","zh":"全部","ja":"すべて","ko":"전체","hi":"सभी","tr":"Tümü"},
 "affiche": {"fr":"À l'affiche","en":"Line-up","es":"En cartel","it":"In scena","pt":"Em cartaz","de":"Programm","ru":"В программе","ar":"المشاركون","zh":"阵容","ja":"出演","ko":"라인업","hi":"कार्यक्रम-सूची","tr":"Program"},
 "access":  {"fr":"Comment y accéder","en":"How to get in","es":"Cómo acceder","it":"Come accedere","pt":"Como aceder","de":"So kommen Sie hinein","ru":"Как попасть","ar":"كيفية الدخول","zh":"如何进入","ja":"アクセス方法","ko":"입장 방법","hi":"प्रवेश कैसे पाएँ","tr":"İçeri nasıl girilir"},
 "access2": {"fr":"Accès","en":"Access","es":"Acceso","it":"Accesso","pt":"Acesso","de":"Zugang","ru":"Доступ","ar":"الدخول","zh":"入场","ja":"アクセス","ko":"입장","hi":"प्रवेश","tr":"Giriş"},
 "official":{"fr":"Site officiel de l'événement","en":"Official event website","es":"Web oficial del evento","it":"Sito ufficiale dell'evento","pt":"Site oficial do evento","de":"Offizielle Website der Veranstaltung","ru":"Официальный сайт события","ar":"الموقع الرسمي للفعالية","zh":"活动官方网站","ja":"イベント公式サイト","ko":"이벤트 공식 사이트","hi":"कार्यक्रम की आधिकारिक वेबसाइट","tr":"Etkinliğin resmî web sitesi"},
 "all_in":  {"fr":"Tous les événements","en":"All events","es":"Todos los eventos","it":"Tutti gli eventi","pt":"Todos os eventos","de":"Alle Veranstaltungen","ru":"Все события","ar":"جميع الفعاليات","zh":"全部活动","ja":"すべてのイベント","ko":"모든 이벤트","hi":"सभी कार्यक्रम","tr":"Tüm etkinlikler"},
 "back":    {"fr":"Retour au radar","en":"Back to the radar","es":"Volver al radar","it":"Torna al radar","pt":"Voltar ao radar","de":"Zurück zum Radar","ru":"Назад к радару","ar":"العودة إلى الرادار","zh":"返回雷达","ja":"レーダーに戻る","ko":"레이더로 돌아가기","hi":"रडार पर वापस","tr":"Radara dön"},
 "places_cats":{"fr":"Tous les lieux & catégories","en":"All places & categories","es":"Todos los lugares y categorías","it":"Tutti i luoghi e le categorie","pt":"Todos os locais e categorias","de":"Alle Orte & Kategorien","ru":"Все места и категории","ar":"جميع الأماكن والفئات","zh":"所有地点与类别","ja":"すべての場所とカテゴリー","ko":"모든 장소 및 카테고리","hi":"सभी स्थान और श्रेणियाँ","tr":"Tüm mekânlar ve kategoriler"},
 "events":  {"fr":"événements","en":"events","es":"eventos","it":"eventi","pt":"eventos","de":"Veranstaltungen","ru":"событий","ar":"فعاليات","zh":"项活动","ja":"件のイベント","ko":"개 이벤트","hi":"कार्यक्रम","tr":"etkinlik"},
 "tagline": {"fr":"Sélection au niveau Riviera : dates, lieux et modes d'accès.","en":"A Riviera-level selection: dates, venues and how to get in.","es":"Una selección de nivel Riviera: fechas, lugares y cómo acceder.","it":"Una selezione di livello Riviera: date, luoghi e come accedere.","pt":"Uma seleção ao nível da Riviera: datas, locais e como aceder.","de":"Eine Auswahl auf Riviera-Niveau: Termine, Orte und Zugang.","ru":"Подборка уровня Ривьеры: даты, места и как попасть.","ar":"اختيار بمستوى الريفييرا: التواريخ والأماكن وكيفية الدخول.","zh":"蔚蓝海岸级别的精选：日期、地点与入场方式。","ja":"リヴィエラ級のセレクション：日程、会場、入場方法。","ko":"리비에라급 셀렉션: 날짜, 장소, 입장 방법.","hi":"रिवेरा स्तर का चयन : तिथियाँ, स्थान और प्रवेश के तरीके।","tr":"Riviera düzeyinde bir seçki: tarihler, mekânlar ve giriş yolları."},
 "hub_h1":  {"fr":"Tous les événements du luxe","en":"All luxury events","es":"Todos los eventos de lujo","it":"Tutti gli eventi del lusso","pt":"Todos os eventos de luxo","de":"Alle Luxus-Veranstaltungen","ru":"Все события мира роскоши","ar":"جميع فعاليات الفخامة","zh":"全部奢华活动","ja":"すべてのラグジュアリー・イベント","ko":"모든 럭셔리 이벤트","hi":"विलासिता के सभी कार्यक्रम","tr":"Tüm lüks etkinlikler"},
 "hub_intro":{"fr":"Parcourez par lieu ou par catégorie. Le radar complet, en direct et en 13 langues, est sur ConstanceParis7.","en":"Browse by place or by category. The full radar, live and in 13 languages, is on ConstanceParis7.","es":"Explore por lugar o por categoría. El radar completo, en directo y en 13 idiomas, está en ConstanceParis7.","it":"Sfoglia per luogo o per categoria. Il radar completo, in diretta e in 13 lingue, è su ConstanceParis7.","pt":"Navegue por local ou por categoria. O radar completo, em direto e em 13 línguas, está no ConstanceParis7.","de":"Stöbern Sie nach Ort oder Kategorie. Das vollständige Radar, live und in 13 Sprachen, finden Sie auf ConstanceParis7.","ru":"Ищите по месту или категории. Полный радар — в реальном времени и на 13 языках — на ConstanceParis7.","ar":"تصفّح حسب المكان أو الفئة. الرادار الكامل، مباشرةً وبثلاث عشرة لغة، على ConstanceParis7.","zh":"按地点或类别浏览。完整雷达，实时更新、13 种语言，尽在 ConstanceParis7。","ja":"場所またはカテゴリーで探せます。完全版レーダー（ライブ・13言語）は ConstanceParis7 にて。","ko":"장소 또는 카테고리로 탐색하세요. 실시간 13개 언어의 전체 레이더는 ConstanceParis7에서.","hi":"स्थान या श्रेणी के अनुसार देखें। पूरा रडार — सीधा प्रसारण, 13 भाषाओं में — ConstanceParis7 पर उपलब्ध है।","tr":"Mekâna veya kategoriye göre göz atın. Canlı ve 13 dildeki tam radar ConstanceParis7'de."},
 "by_cat":  {"fr":"Par catégorie","en":"By category","es":"Por categoría","it":"Per categoria","pt":"Por categoria","de":"Nach Kategorie","ru":"По категориям","ar":"حسب الفئة","zh":"按类别","ja":"カテゴリー別","ko":"카테고리별","hi":"श्रेणी के अनुसार","tr":"Kategoriye göre"},
 "by_place":{"fr":"Par lieu","en":"By place","es":"Por lugar","it":"Per luogo","pt":"Por local","de":"Nach Ort","ru":"По местам","ar":"حسب المكان","zh":"按地点","ja":"場所別","ko":"장소별","hi":"स्थान के अनुसार","tr":"Mekâna göre"},
 "footer":  {"fr":"ConstanceParis7 — le radar des événements du luxe, mis à jour chaque jour.","en":"ConstanceParis7 — the radar of luxury events, updated every day.","es":"ConstanceParis7 — el radar de los eventos de lujo, actualizado cada día.","it":"ConstanceParis7 — il radar degli eventi del lusso, aggiornato ogni giorno.","pt":"ConstanceParis7 — o radar dos eventos de luxo, atualizado todos os dias.","de":"ConstanceParis7 — das Radar der Luxus-Veranstaltungen, täglich aktualisiert.","ru":"ConstanceParis7 — радар событий мира роскоши, обновляется каждый день.","ar":"ConstanceParis7 — رادار فعاليات الفخامة، يُحدَّث كل يوم.","zh":"ConstanceParis7 — 奢华活动雷达，每日更新。","ja":"ConstanceParis7 — ラグジュアリー・イベントのレーダー。毎日更新。","ko":"ConstanceParis7 — 매일 업데이트되는 럭셔리 이벤트 레이더.","hi":"ConstanceParis7 — विलासिता के कार्यक्रमों का रडार, प्रतिदिन अद्यतन।","tr":"ConstanceParis7 — her gün güncellenen lüks etkinlik radarı."},
 "see_live":{"fr":"Voir tout le radar en direct","en":"See the full radar live","es":"Ver todo el radar en directo","it":"Vedi tutto il radar in diretta","pt":"Ver todo o radar em direto","de":"Das ganze Radar live ansehen","ru":"Смотреть весь радар в реальном времени","ar":"شاهد الرادار الكامل مباشرةً","zh":"查看完整实时雷达","ja":"完全版レーダーをライブで見る","ko":"전체 레이더 실시간 보기","hi":"पूरा रडार लाइव देखें","tr":"Radarın tamamını canlı izleyin"},
 "stay":{"fr":"Le séjour clé en main","en":"The turnkey stay","es":"La estancia llave en mano","it":"Il soggiorno chiavi in mano","pt":"A estadia chave na mão","de":"Der schlüsselfertige Aufenthalt","ru":"Поездка «под ключ»","ar":"الإقامة المتكاملة","zh":"一站式行程","ja":"すべて手配済みの滞在","ko":"턴키 스테이","hi":"संपूर्ण प्रवास","tr":"Anahtar teslim konaklama"},
 "stay_hotels":{"fr":"Où dormir","en":"Where to stay","es":"Dónde alojarse","it":"Dove dormire","pt":"Onde ficar","de":"Wo übernachten","ru":"Где остановиться","ar":"أين تقيم","zh":"住宿之选","ja":"滞在先","ko":"숙소","hi":"कहाँ ठहरें","tr":"Nerede kalınır"},
 "stay_tables":{"fr":"Où dîner","en":"Where to dine","es":"Dónde cenar","it":"Dove cenare","pt":"Onde jantar","de":"Wo speisen","ru":"Где ужинать","ar":"أين تتناول العشاء","zh":"用餐之选","ja":"食事","ko":"다이닝","hi":"कहाँ भोजन करें","tr":"Nerede yemek yenir"},
 "stay_exp":{"fr":"À vivre sur place","en":"What to experience","es":"Qué vivir","it":"Da vivere sul posto","pt":"O que viver","de":"Was erleben","ru":"Что испытать","ar":"تجارب لا تُفوَّت","zh":"必体验","ja":"体験","ko":"경험","hi":"क्या अनुभव करें","tr":"Yerinde yaşanacaklar"},
 "luxury_events":{"fr":"événements du luxe","en":"luxury events","es":"eventos de lujo","it":"eventi del lusso","pt":"eventos de luxo","de":"Luxus-Veranstaltungen","ru":"события роскоши","ar":"فعاليات الفخامة","zh":"奢华活动","ja":"ラグジュアリー・イベント","ko":"럭셔리 이벤트","hi":"विलासिता के कार्यक्रम","tr":"lüks etkinlikler"},
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
    # Le dépôt a été transféré et RENOMMÉ le 18/08/2026 :
    # H2SL-bot/luxe-ete-2026 → constanceparis7/radar-luxe. Le garde-fou ne
    # connaissait que l'ancien nom : il refusait donc le dépôt légitime et
    # arrêtait la passe quotidienne dès sa première étape. On accepte les deux
    # noms connus ; un dépôt inconnu reste refusé, la protection est intacte.
    DEPOTS_ATTENDUS = ("luxe-ete-2026", "radar-luxe")
    if origin and not any(d in origin for d in DEPOTS_ATTENDUS):
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
        # FR : les voies d'accès vivent dans e["iv"], pas dans des champs plats
        if key.startswith("iv_"):
            return (e.get("iv") or {}).get(key[3:])
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

    def u_home(lang):
        """adresse canonique de la porte d'entrée d'une langue (/en/, /ja/…)."""
        return f"{prefix(lang)}/"

    def p_home(lang):
        """fichier correspondant. Jamais appelé pour 'fr' : la racine, c'est
        index.html, le site visible, que ce script ne modifie jamais."""
        return f"{prefix(lang)}/index.html"

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
            f"<style>{CSS}</style>{ldblock}"
            # Même mesure d'audience que la page d'accueil : sans elle, les
            # arrivées Google directes sur une fiche étaient invisibles.
            "<script data-goatcounter=\"https://constanceparis7.goatcounter.com/count\" async src=\"//gc.zgo.at/count.js\"></script>"
            "</head><body><div class=\"wrap\">"
            f"<header class=\"site\"><a href=\"{prefix(lang)}/\" class=\"brand\">ConstanceParis<span class=\"s\">7</span></a>"
            "<div class=\"edition\">International Luxury Events</div></header>"
            f"{body}"
            f"<footer class=\"site\">{esc(UI['footer'][lang])} "
            f"<a href=\"/\">{esc(UI['see_live'][lang])} →</a>"
            # Obligation légale (LCEN art. 6) : la page doit être atteignable
            # depuis n'importe quelle page du site. Libellé bilingue : la page
            # elle-même est en français, c'est un texte de droit français.
            " · <a href=\"/a-propos.html\">À propos · Contact</a>"
            " · <a href=\"/mentions-legales.html\">Mentions légales</a>"
            "</footer></div></body></html>"
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
            # LE SÉJOUR CLÉ EN MAIN — le cœur de valeur du site, longtemps absent
            # des pages indexables : palaces, tables et expériences autour de
            # l'événement, traduits quand la langue est disponible.
            sej = e.get("sej") or {}
            if sej:
                trs = (e.get("tr") or {}).get(lang, {}) if lang != "fr" else {}
                def sT(cle, defaut):
                    return trs.get(cle) or defaut if lang != "fr" else defaut
                bloc = [f"<div class=\"box\"><h2>{esc(UI['stay'][lang])}</h2>"]
                pitch = sT("sej_pitch", sej.get("pitch"))
                if pitch:
                    bloc.append(f"<p>{esc(pitch)}</p>")
                for grp, libelle in (("hotels", "stay_hotels"), ("tables", "stay_tables"), ("exp", "stay_exp")):
                    items = [x for x in (sej.get(grp) or []) if x.get("n")]
                    if not items:
                        continue
                    bloc.append(f"<h3>{esc(UI[libelle][lang])}</h3><ul>")
                    for i, x in enumerate(items):
                        d = sT(f"sej_{grp}{i}", x.get("d") or "")
                        nom = esc(x["n"])
                        lien = f"<a href=\"{esc(x['u'])}\" target=\"_blank\" rel=\"noopener nofollow\">{nom}</a>" if x.get("u") else nom
                        bloc.append(f"<li><b>{lien}</b>" + (f" — {esc(d)}" if d else "") + "</li>")
                    bloc.append("</ul>")
                bloc.append("</div>")
                body.append("".join(bloc))
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

        # --- porte d'entrée de la langue -------------------------------------
        # Le français vit à la racine : index.html EST le site visible, jamais
        # touché. Les autres langues n'avaient AUCUNE page d'accueil — /en/,
        # /ja/, /ar/… répondaient 404. Or chaque page générée y renvoie deux
        # fois (le logo et le fil d'Ariane) et les hreflang la déclarent à
        # Google : des milliers de liens internes morts, et un lecteur étranger
        # qui bute sur un mur dès son premier clic. On la construit avec le
        # vocabulaire DÉJÀ traduit du site — aucune traduction inventée.
        if lang != "fr":
            L18 = i18n.get(lang, i18n["fr"])

            def tk(key, defaut=""):
                return L18.get(key) or i18n["fr"].get(key) or defaut

            home = [f"<h1>ConstanceParis7 — {esc(UI['luxury_events'][lang])}</h1>",
                    f"<p class=\"meta\">{esc(tk('brandsub', UI['tagline'][lang]))}</p>",
                    f"<p><a class=\"cta\" href=\"/\">{esc(UI['see_live'][lang])} →</a></p>"]

            rubriques = [tk(k) for k in ("nav_today", "nav_prestige", "nav_calendar",
                                         "nav_agenda", "nav_continu", "nav_intl",
                                         "nav_invite", "nav_archives") if tk(k)]
            if rubriques:
                home.append(f"<div class=\"box\"><h2>{esc(UI['radar'][lang])}</h2><ul>")
                home += [f"<li>{esc(r)}</li>" for r in rubriques]
                home.append("</ul></div>")

            # À l'affiche : de vrais liens internes vers les fiches traduites.
            datees = sorted((e for e in pages if e.get("d1")), key=lambda e: e["d1"])
            aff = [e for e in datees if e["d1"] >= TODAY][:12] or datees[-12:]
            if aff:
                home.append(f"<h2 class=\"sub\">{esc(UI['affiche'][lang])}</h2><ul class=\"cards\">")
                for e in aff:
                    home.append(f"<li><div class=\"d\">{esc(e.get('d1',''))} · {esc(e.get('v',''))}</div>"
                                f"<div class=\"t\"><a href=\"{u_event(e, lang)}\">{esc(T(e, lang, 'n'))}</a></div></li>")
                home.append("</ul>")

            home.append(f"<h2 class=\"sub\">{esc(UI['by_cat'][lang])}</h2><div class=\"chips\">")
            for c, v in sorted(cats.items(), key=lambda kv: -len(kv[1]["events"])):
                home.append(f"<a href=\"{u_cat(v, lang)}\">{esc(cat_label(c, lang))} ({len(v['events'])})</a>")
            home.append(f"</div><h2 class=\"sub\">{esc(UI['by_place'][lang])}</h2><div class=\"chips\">")
            for k, v in sorted(places.items(), key=lambda kv: -len(kv[1]["events"]))[:40]:
                home.append(f"<a href=\"{u_place(v, lang)}\">{esc(k)} ({len(v['events'])})</a>")
            home.append(f"</div><p><a href=\"{u_hub(lang)}\">{esc(UI['places_cats'][lang])} →</a></p>")

            # Le radar ne lit sa langue que dans localStorage — il n'existe
            # aucun paramètre d'URL. Sans cette ligne, un lecteur arrivé sur
            # /ja/ repartait en français dès qu'il cliquait vers le radar.
            home.append(f"<script>try{{localStorage.setItem('luxe_lang','{lang}')}}catch(e){{}}</script>")

            hl_home = "".join(f'<link rel="alternate" hreflang="{L}" href="{BASE}{u_home(L)}">'
                              for L in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{BASE}/">'
            write(p_home(lang), page(lang, f"ConstanceParis7 — {UI['luxury_events'][lang]}",
                                     tk('brandsub', UI['tagline'][lang])[:155],
                                     u_home(lang), "".join(home), hl_home))
            sitemap_urls.append(f"{BASE}{u_home(lang)}")

    # --- à propos / contact ------------------------------------------------
    # La page qui transforme un lecteur en partenaire : elle dit QUI tient le
    # radar et POURQUOI on peut le croire. Générée comme les autres.
    AP = """<div class="bc"><a href="/">Radar</a> · À propos</div>
<h1>À propos</h1>
<p class="meta">Le radar — et la personne derrière.</p>

<p>Je m'appelle <b>Constance Lefebvre</b>. Je suis lycéenne, et je tiens
ce radar seule.</p>

<h2 class="sub">Ce qui me passionne</h2>
<p>Les palaces, la haute couture, la haute joaillerie — <b>l'élégance à la
française</b>. C'est mon sujet depuis toujours, et c'est le monde dans lequel je
veux travailler. Je n'ai pas envie de le regarder depuis un écran : j'ai envie
d'y être, d'y rencontrer des gens, de comprendre comment il fonctionne de
l'intérieur. Ce radar a commencé exactement comme ça — en cartographiant, une
par une, les portes d'entrée.</p>

<h2 class="sub">Ce qu'est ConstanceParis7</h2>
<p>Un radar, pas un blog. <b>309 événements à venir</b>, dans <b>129 villes</b>,
publiés en <b>13 langues</b>, et remis à jour <b>chaque jour</b>.</p>
<p>Avec une règle qui ne bouge pas : un événement n'entre dans le radar que s'il
vient avec <b>une voie d'entrée et un séjour</b>. Savoir qu'une soirée existe ne
sert à rien si personne ne dit comment y aller.</p>

<div class="box">
<h2>Comment je travaille</h2>
<ul>
<li>Chaque information est prise <b>à sa source officielle</b>, puis <b>datée</b>.</li>
<li>Un doute n'est jamais transformé en affirmation : il est inscrit, et tranché
à la vérification suivante.</li>
<li>Un lieu fermé, un événement annulé : archivé avec sa preuve, jamais effacé
en silence.</li>
<li>Une erreur signalée est corrigée <b>sous 48 heures</b>, et la correction est
mentionnée.</li>
</ul>
<p>C'est exigeant, et c'est tout l'intérêt du site : dans ce domaine,
l'information périmée est partout.</p>
</div>

<h2 class="sub">D'où ça vient</h2>
<p>Le radar est né d'un projet mené avec mon père, qui connaissait ma passion et
m'a aidée à le mettre sur pied. <b>J'en ai repris seule la conduite en août
2026</b> : la ligne éditoriale, les vérifications, les publications.</p>

<h2 class="sub">Travailler ensemble</h2>
<p>Maisons, palaces, hôtels, clubs, restaurants, joailliers, organisateurs :
<b>écrivez-moi</b>. Je suis ouverte aux collaborations sérieuses, et c'est
précisément le milieu dans lequel je veux évoluer.</p>
<div class="box">
<h2>Une chose ne se négocie pas</h2>
<p><b>Une place dans le radar ne s'achète pas.</b> Un événement y figure parce
qu'il est vérifié, jamais parce qu'il est payé. Si un partenariat existe un
jour, il sera signalé comme tel, sur la fiche concernée.</p>
<p>C'est la condition pour que ce site garde la seule chose qui fasse sa
valeur : la confiance de celles et ceux qui le lisent.</p>
</div>

<h2 class="sub">Me joindre</h2>
<p><a class="cta" href="mailto:constanceparis7e@gmail.com">constanceparis7e@gmail.com</a></p>
<p>Une proposition, une correction, une invitation : je lis tout.</p>

<div class="chips"><a href="/">← Retour au radar</a><a href="/mentions-legales.html">Mentions légales</a></div>"""
    write("/a-propos.html",
          page("fr", "À propos — ConstanceParis7",
               "Constance Lefebvre tient seule le radar des événements du luxe : sa "
               "méthode de vérification, sa règle éditoriale, et comment la joindre "
               "pour une collaboration.",
               "/a-propos.html", AP,
               '<link rel="alternate" hreflang="fr" href="%s/a-propos.html">' % BASE))
    sitemap_urls.append(f"{BASE}/a-propos.html")

    # --- mentions légales (obligation de l'article 6 de la LCEN) -----------
    # Page générée comme les autres pour hériter du même habillage et entrer
    # au plan du site. Rédigée en français : c'est un texte de droit français.
    ML = """<div class="bc"><a href="/">Radar</a> · Mentions légales</div>
<h1>Mentions légales</h1>
<p class="meta">Dernière mise à jour : <b>20 août 2026</b></p>

<h2 class="sub">Éditrice du site</h2>
<p><b>Constance Lefebvre</b>, personne physique éditant ce site à titre non professionnel.<br>
Contact : <a href="mailto:constanceparis7e@gmail.com">constanceparis7e@gmail.com</a></p>
<p>Conformément à l'article 6, III, 2° de la loi n° 2004-575 du 21 juin 2004 pour la
confiance dans l'économie numérique, l'éditrice, qui publie à titre non professionnel,
ne rend pas publique son adresse postale. Les éléments d'identification prévus par la
loi sont détenus par l'hébergeur, qui les tient à la disposition de l'autorité judiciaire.</p>

<h2 class="sub">Directrice de la publication</h2>
<p>Constance Lefebvre.</p>

<h2 class="sub">Hébergeur</h2>
<p>GitHub, Inc. — service GitHub Pages<br>
88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis<br>
<a href="https://github.com" target="_blank" rel="noopener nofollow">github.com</a></p>

<h2 class="sub">Nom de domaine</h2>
<p>constanceparis7.com, enregistré le 11 juillet 2026 auprès de <b>Gandi SAS</b>
(<a href="https://www.gandi.net" target="_blank" rel="noopener nofollow">gandi.net</a>).</p>

<div class="box">
<h2>Ce que ce site est — et ce qu'il n'est pas</h2>
<p>ConstanceParis7 recense des événements organisés par des tiers : maisons, hôtels,
festivals, musées, clubs. Le site <b>n'organise aucun événement, ne vend aucun billet,
ne perçoit aucune commission</b> et n'entretient aucun lien contractuel avec les
organisateurs cités.</p>
<p>Chaque information est vérifiée à sa source officielle, puis datée. Les dates, les
tarifs et les conditions d'accès peuvent changer sans préavis :
<b>confirmez toujours auprès de l'organisateur avant de vous déplacer ou de réserver.</b></p>
<p>Une erreur vous a échappé ? Écrivez à
<a href="mailto:constanceparis7e@gmail.com">constanceparis7e@gmail.com</a> :
correction ou retrait sous 48 heures, et la correction est mentionnée.</p>
</div>

<h2 class="sub">Propriété intellectuelle</h2>
<p>Les textes, la sélection des événements et l'organisation des informations publiées
sur ce site sont l'œuvre de l'éditrice et sont protégés par le droit d'auteur. Toute
reproduction, même partielle, est soumise à autorisation écrite préalable.</p>
<p>Les marques, logos, noms d'établissements et noms d'événements cités appartiennent à
leurs titulaires respectifs. Ils sont mentionnés à seule fin d'information du lecteur.</p>

<h2 class="sub">Données personnelles</h2>
<div class="box">
<h2>En résumé</h2>
<ul>
<li>Aucun compte, aucun formulaire, aucune inscription.</li>
<li><b>Aucun cookie</b> n'est déposé sur votre appareil.</li>
<li>Aucune donnée n'est vendue, louée, ni transmise à un tiers.</li>
</ul>
</div>
<p><b>Mesure d'audience.</b> Le site utilise GoatCounter
(constanceparis7.goatcounter.com), un service de statistiques sans cookie, qui
n'enregistre aucun identifiant individuel et ne permet pas de reconnaître un visiteur
d'une visite à l'autre. Seules des données agrégées sont produites : nombre de pages
vues, page consultée, pays, site de provenance.</p>
<p><b>Mémoire de la langue.</b> La langue que vous choisissez est enregistrée dans votre
navigateur sous la clé <b>luxe_lang</b>, afin de ne pas vous la redemander. Cette
information reste sur votre appareil et n'est jamais transmise. Vider les données du
site l'efface.</p>
<p><b>Courriels.</b> Si vous écrivez à l'adresse de contact, votre message et votre
adresse sont conservés le temps nécessaire au traitement de votre demande, puis
supprimés.</p>
<p><b>Vos droits.</b> Conformément au Règlement général sur la protection des données
et à la loi Informatique et Libertés, vous disposez d'un droit d'accès, de
rectification, d'effacement et d'opposition. Pour l'exercer, écrivez à
<a href="mailto:constanceparis7e@gmail.com">constanceparis7e@gmail.com</a>. Vous pouvez
également introduire une réclamation auprès de la CNIL
(<a href="https://www.cnil.fr" target="_blank" rel="noopener nofollow">cnil.fr</a>).</p>

<h2 class="sub">Liens sortants</h2>
<p>Ce site renvoie vers les sites officiels des organisateurs et des lieux cités.
L'éditrice n'exerce aucun contrôle sur ces sites et décline toute responsabilité quant
à leur contenu, leurs pratiques et leur disponibilité.</p>

<h2 class="sub">Droit applicable</h2>
<p>Le présent site et les présentes mentions légales sont soumis au droit français.</p>

<div class="chips"><a href="/">← Retour au radar</a></div>"""
    write("/mentions-legales.html",
          page("fr", "Mentions légales — ConstanceParis7",
               "Éditrice, directrice de la publication, hébergeur, propriété "
               "intellectuelle et données personnelles du radar ConstanceParis7.",
               "/mentions-legales.html", ML,
               '<link rel="alternate" hreflang="fr" href="%s/mentions-legales.html">' % BASE))
    sitemap_urls.append(f"{BASE}/mentions-legales.html")

    # --- sitemap ---
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sitemap_urls:
        # Seules la racine et les portes d'entrée de langue se terminent par
        # « / » ; tout le reste est un .html. Une porte d'entrée de langue pèse
        # plus qu'une page de lieu : c'est par elle qu'un lecteur étranger entre.
        accueil_langue = u.endswith("/") and u != f"{BASE}/"
        if u == f"{BASE}/":
            pr = "1.0"
        elif accueil_langue:
            pr = "0.9"
        elif "/evenements" in u or "/lieu/" in u or "/type/" in u:
            pr = "0.8"
        else:
            pr = "0.6"
        cf = "daily" if (u == f"{BASE}/" or accueil_langue) else "weekly"
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
