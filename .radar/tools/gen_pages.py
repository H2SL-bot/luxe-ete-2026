#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

_RX_VERIF = re.compile(r"(?:v[ée]rifi\w*|contr[oô]l[ée]\w*|checked)[^0-9]{0,30}?(\d{1,2}/\d{1,2}/\d{4})", re.I)
def date_verif(e):
    """Dernière date de vérification ÉCRITE dans les sources de la fiche ; None sinon.
    Constat du 26/08/2026 : il n'existe pas de champ structuré (dc = dress code),
    mais 122+ fiches portent « vérifié le JJ/MM/AAAA » dans so ou iv. On affiche
    seulement ce qui est écrit : pas de date trouvée, pas de badge."""
    textes = [str(e.get("so") or "")]
    iv = e.get("iv")
    if isinstance(iv, dict):
        textes += [str(v) for v in iv.values() if isinstance(v, str)]
    meilleurs = []
    for tx in textes:
        for m in _RX_VERIF.finditer(tx):
            j, mo, a = m.group(1).split("/")
            try:
                meilleurs.append((int(a), int(mo), int(j)))
            except ValueError:
                pass
    if not meilleurs:
        return None
    a, mo, j = max(meilleurs)
    return f"{j:02d}/{mo:02d}/{a}"

def note_radar(e):
    """La Note du radar (institution du 27/08/2026) : le score du Classement
    Prestige, sorti de l'ombre et porté sur chaque fiche. Portage FIDÈLE de
    la formule du JS de l'accueil (une seule source de vérité) : quatre
    critères publiés depuis l'origine dans sec_prestige_intro, avec leurs
    poids : exclusivité de l'accès 4, personnalités attendues 3, lieu 2,
    proximité de la date 1 (recalculée à chaque génération). On note la
    porte, pas la fête : des faits documentés, jamais un ressenti."""
    sv, sp, sl = e.get("sv"), e.get("sp"), e.get("sl")
    if sv is None or sp is None or sl is None:
        return None
    arrondi = lambda x: int(x + 0.5)  # Math.round du JS, pas le round bancaire
    t = TODAY
    d1, d2 = str(e.get("d1") or ""), str(e.get("d2") or "")
    try:
        if d1 <= t <= d2:
            ds = 100
        elif d1 > t:
            j = (date.fromisoformat(d1) - date.fromisoformat(t)).days
            ds = max(15, arrondi(100 - 2.2 * j))
        else:
            j = (date.fromisoformat(t) - date.fromisoformat(d2)).days
            ds = max(0, arrondi(55 - 4 * j))
    except ValueError:
        return None
    return arrondi(0.4 * sv + 0.3 * sp + 0.2 * sl + 0.1 * ds)

def diamants(n):
    """Mêmes paliers que diamonds() du JS de l'accueil."""
    return "✦" * (5 if n >= 88 else 4 if n >= 76 else 3 if n >= 62 else 2 if n >= 48 else 1)

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
 "verified":{"fr":"Vérifié à la source le","en":"Verified at the source on","es":"Verificado en la fuente el","it":"Verificato alla fonte il","pt":"Verificado na fonte a","de":"An der Quelle geprüft am","ru":"Проверено по источнику:","ar":"تم التحقق من المصدر بتاريخ","zh":"已于源头核实：","ja":"公式情報で確認：","ko":"공식 출처 확인:","hi":"स्रोत से सत्यापित:","tr":"Kaynağından doğrulandı:"},
 "radar":   {"fr":"Radar","en":"Radar","es":"Radar","it":"Radar","pt":"Radar","de":"Radar","ru":"Радар","ar":"الرادار","zh":"雷达","ja":"レーダー","ko":"레이더","hi":"रडार","tr":"Radar"},
 "note":    {"fr":"Note du radar","en":"Radar score","es":"Nota del radar","it":"Voto del radar","pt":"Nota do radar","de":"Radar-Note","ru":"Оценка радара","ar":"تقييم الرادار","zh":"雷达评分","ja":"レーダースコア","ko":"레이더 점수","hi":"रडार स्कोर","tr":"Radar notu"},
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
 "hub_intro":{"fr":"Parcourez par lieu ou par catégorie. Le radar complet, en direct et en 13 langues, est sur ConstanceParis7.","en":"Browse by place or by category. The full radar, live and in 13 languages, is on ConstanceParis7.","es":"Explore por lugar o por categoría. El radar completo, en directo y en 13 idiomas, está en ConstanceParis7.","it":"Sfoglia per luogo o per categoria. Il radar completo, in diretta e in 13 lingue, è su ConstanceParis7.","pt":"Navegue por local ou por categoria. O radar completo, em direto e em 13 línguas, está no ConstanceParis7.","de":"Stöbern Sie nach Ort oder Kategorie. Das vollständige Radar, live und in 13 Sprachen, finden Sie auf ConstanceParis7.","ru":"Ищите по месту или категории. Полный радар, в реальном времени и на 13 языках, на ConstanceParis7.","ar":"تصفّح حسب المكان أو الفئة. الرادار الكامل، مباشرةً وبثلاث عشرة لغة، على ConstanceParis7.","zh":"按地点或类别浏览。完整雷达，实时更新、13 种语言，尽在 ConstanceParis7。","ja":"場所またはカテゴリーで探せます。完全版レーダー（ライブ・13言語）は ConstanceParis7 にて。","ko":"장소 또는 카테고리로 탐색하세요. 실시간 13개 언어의 전체 레이더는 ConstanceParis7에서.","hi":"स्थान या श्रेणी के अनुसार देखें। पूरा रडार — सीधा प्रसारण, 13 भाषाओं में — ConstanceParis7 पर उपलब्ध है।","tr":"Mekâna veya kategoriye göre göz atın. Canlı ve 13 dildeki tam radar ConstanceParis7'de."},
 "by_cat":  {"fr":"Par catégorie","en":"By category","es":"Por categoría","it":"Per categoria","pt":"Por categoria","de":"Nach Kategorie","ru":"По категориям","ar":"حسب الفئة","zh":"按类别","ja":"カテゴリー別","ko":"카테고리별","hi":"श्रेणी के अनुसार","tr":"Kategoriye göre"},
 "by_place":{"fr":"Par lieu","en":"By place","es":"Por lugar","it":"Per luogo","pt":"Por local","de":"Nach Ort","ru":"По местам","ar":"حسب المكان","zh":"按地点","ja":"場所別","ko":"장소별","hi":"स्थान के अनुसार","tr":"Mekâna göre"},
 "footer":  {"fr":"ConstanceParis7 · le radar des événements du luxe, mis à jour chaque jour.","en":"ConstanceParis7 · the radar of luxury events, updated every day.","es":"ConstanceParis7 · el radar de los eventos de lujo, actualizado cada día.","it":"ConstanceParis7 · il radar degli eventi del lusso, aggiornato ogni giorno.","pt":"ConstanceParis7 · o radar dos eventos de luxo, atualizado todos os dias.","de":"ConstanceParis7 · das Radar der Luxus-Veranstaltungen, täglich aktualisiert.","ru":"ConstanceParis7 · радар событий мира роскоши, обновляется каждый день.","ar":"ConstanceParis7 · رادار فعاليات الفخامة، يُحدَّث كل يوم.","zh":"ConstanceParis7 · 奢华活动雷达，每日更新。","ja":"ConstanceParis7 · ラグジュアリー・イベントのレーダー。毎日更新。","ko":"ConstanceParis7 · 매일 업데이트되는 럭셔리 이벤트 레이더.","hi":"ConstanceParis7 · विलासिता के कार्यक्रमों का रडार, प्रतिदिन अद्यतन।","tr":"ConstanceParis7 · her gün güncellenen lüks etkinlik radarı."},
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

    # Constat de la relecture native du 24/08/2026 : les libellés de lieux
    # (accueils, hub, pages lieu, fil de navigation) sortaient en FRANÇAIS dans
    # les 12 langues, alors que villes-i18n.json et geo-i18n.json existent.
    # Un Italien lisait « Venise » et « Sardaigne » sur sa propre page.
    _RAD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _DICOS_LIEUX = []
    for _nom in ("geo-i18n.json", "villes-i18n.json"):
        try:
            with open(os.path.join(_RAD, _nom), encoding="utf-8") as _f:
                _DICOS_LIEUX.append(json.load(_f))
        except Exception:
            pass  # un dictionnaire illisible ne doit jamais casser la génération

    def place_label(k, lang):
        """libellé d'un lieu dans la langue demandée ; repli : la clé française."""
        if lang == "fr" or not k:
            return k

    # --- Pages éditoriales MULTILINGUES (Méthode, Moments, Adresses, Vestiaire).
    # 26/08/2026 : nées en français ; 13 langues le même soir, à la demande de
    # Constance. Le français ci-dessous est la RÉFÉRENCE ; les traductions
    # vivent dans .radar/pages-i18n.json (produites par vague d'agents,
    # posées sous garde-fous). Langue absente => repli français, jamais de vide.
    PFR = {
     "bc_moments": "Moments", "bc_adresses": "Adresses", "bc_vestiaire": "Vestiaire", "bc_methode": "Méthode",
     "explorer": "Explorer",
     "m_h1": "La méthode",
     "m_meta": "Comment ce radar est fabriqué, et pourquoi vous pouvez vous y fier.",
     "m_desc": "Les règles de vérification du radar : sources officielles, dates prouvées, doutes inscrits, corrections sous 48 heures.",
     "m_intro": "Ce site est un travail de vérification avant d'être un travail de publication. Voici les règles qui le gouvernent. Elles ne souffrent pas d'exception.",
     "m_rules_t": "Les règles",
     "m_r1": "<b>Une date est vraie, ou elle n'existe pas.</b> Chaque information est prise à sa source officielle, puis datée. Une date de fin n'est jamais posée par défaut : elle est lue sur la source, ou le doute est écrit.",
     "m_r2": "<b>Un doute n'est jamais publié comme une certitude.</b> Il est inscrit à un registre, puis tranché à la vérification suivante.",
     "m_r3": "<b>Choisir est un art.</b> Le radar ne liste pas tout ce qui existe : il retient ce qui mérite de l'être, au niveau d'exigence de la Riviera.",
     "m_r4": "<b>Rien ne s'efface en silence.</b> Un lieu fermé, un événement annulé : archivé avec sa preuve. Les archives restent consultables.",
     "m_r5": "<b>Une place ne s'achète pas.</b> Aucun événement ne figure ici contre paiement. Les partenariats, s'ils existent, sont signalés sur la page concernée.",
     "m_r6": "<b>Une erreur signalée est corrigée sous 48 heures</b>, et la correction est mentionnée.",
     "m_signaler": "Signaler une erreur",
     "m_badge_t": "Le badge « Vérifié à la source »",
     "m_badge_p": "Sur les pages d'événement, la mention <b>« ✓ Vérifié à la source le… »</b> indique la date à laquelle l'information a été confrontée pour la dernière fois à sa source officielle. Elle ne s'affiche que lorsque cette vérification est consignée : pas de preuve, pas de badge.",
     "m_langs_t": "Les langues",
     "m_langs_p": "Chaque page existe en 13 langues. Le français est la référence : en cas de divergence, c'est lui qui fait foi, et la traduction est corrigée.",
     "a_h1": "Les Adresses",
     "a_meta": "Les lieux qui ne dépendent pas d'une date : clubs, beach clubs, dîners-spectacles. Comment on y entre, ce que ça coûte, à qui écrire.",
     "a_desc": "Clubs, beach clubs et dîners-spectacles du radar : les lieux qui comptent, et comment on y entre.",
     "a_p1": "À Paris, deux institutions se méritent plus qu'elles ne se réservent : le Silencio, club privé sur candidature, et les lieux-scènes du type Hôtel Costes ou Caves du Roy, dont les voies d'entrée sont détaillées dans les guides du radar, sur la page d'accueil.",
     "a_p2": "Un événement se manque ; une adresse se retrouve. Cette page rassemble les lieux du radar dont la porte compte plus que le calendrier : chaque fiche dit la voie d'entrée, vérifiée comme le reste.",
     "v_h1": "Le Vestiaire",
     "v_meta": "Comment s'habiller, événement par événement. Être mal habillée, c'est se voir refuser la porte : le dress code fait partie de la voie d'entrée.",
     "v_desc": "Les dress codes publiés des événements du radar : tenue de soirée, black tie, tenue blanche, chapeaux. Ce qu'on porte, porte par porte.",
     "v_p1": "Les tenues ci-dessous sont celles que les organisateurs publient ou exigent, relevées fiche par fiche. Quand un événement n'apparaît pas ici, c'est que son code vestimentaire n'est pas publié : dans le doute, l'élégance sobre ne se refuse nulle part.",
     "v_ascot_t": "Le cas Royal Ascot",
     "v_ascot_p": "Le dress code le plus codifié du monde change selon l'enclosure : formel (morning dress, chapeaux) en Royal Enclosure et Queen Anne, style estival encouragé au Village, aucune exigence au Windsor. Le détail est sur la fiche",
     "retour": "Retour au radar",
     "mem_h1": "La mémoire du radar",
     "bc_memoire": "Mémoire",
     "bc_protocole": "Protocole",
     "pr_h1": "Le Protocole",
     "pr_desc": "Le savoir-être des événements du luxe : ce que les institutions exigent, publié et vérifié à la source. Galas, ventes aux enchères, bals, courses, clubs privés, foires d'art.",
     "pr_meta": "Savoir entrer ne suffit pas. Le radar dit où aller et comment entrer ; le Vestiaire dit quoi porter ; le Protocole dit comment se tenir.",
     "pr_intro": "Chaque monde a ses règles, et les grandes institutions les publient : codes vestimentaires au centimètre près, horaires immuables, téléphones proscrits. Le Protocole les rassemble, vérifiées à la source, puis y ajoute l'usage : ce qui ne s'écrit nulle part mais se remarque partout.",
     "pr_or_t": "La règle d'or",
     "pr_or_p": "On ne publie ici que deux choses : les règles écrites par les institutions elles-mêmes, consultées à la source, et l'usage que la maison assume comme son propre conseil. Jamais de folklore, jamais de règle inventée.",
     "pr_regles_t": "Ce que les institutions publient",
     "pr_usage_t": "L'usage, selon la maison",
     "pr_radar_t": "Sur le radar",
     "pr_verifie": "Chaque règle est reprise du document publié par l'institution, consulté à son adresse officielle le 27/08/2026.",
     "pr_le-gala_h1": "Le gala",
     "pr_le-gala_desc": "Black tie, white tie, réponse à l'invitation, horaires : le protocole des galas et dîners de charité, vérifié aux sources.",
     "pr_le-gala_intro": "Un gala est une mécanique de précision : une invitation qui appelle une réponse, un code vestimentaire qui ne se discute pas, un déroulé réglé à la minute. Voici ce que publient les autorités de l'étiquette et les maisons qui les donnent.",
     "pr_le-gala_usage": "On répond à une invitation dans les jours qui suivent, jamais la veille. On arrive à l'heure du cocktail, pas à celle du dîner ; on ne change pas de place à table. Pendant la vente aux enchères du gala, on applaudit les lots des autres. Le téléphone reste en poche : un gala se raconte le lendemain, pas en direct.",
     "pr_la-vente-aux-encheres_h1": "La vente aux enchères",
     "pr_la-vente-aux-encheres_desc": "S'enregistrer, lever le paddle, ne jamais annuler : le protocole des ventes aux enchères selon Christie's, Sotheby's et Phillips.",
     "pr_la-vente-aux-encheres_intro": "La salle des ventes est l'un des derniers théâtres à rituel strict du monde du luxe : on s'y enregistre, on y lève un carton numéroté, et chaque geste engage. Les maisons publient leurs règles ; les voici.",
     "pr_la-vente-aux-encheres_usage": "On visite l'exposition avant la vente, et l'on demande avant de toucher. On s'assied avant le premier lot, on garde ses gestes pour soi et l'on lève son paddle franchement : dans une salle des ventes, c'est le commissaire-priseur qu'on regarde. Le silence pendant les lots des autres est la première élégance.",
     "pr_l-opera-et-le-bal_h1": "L'opéra et le bal",
     "pr_l-opera-et-le-bal_desc": "Frac obligatoire, robe longue jusqu'au sol, retardataires placés à l'entracte : le protocole de l'opéra et des grands bals viennois.",
     "pr_l-opera-et-le-bal_intro": "Nulle part le protocole n'est plus explicite qu'à Vienne : les bals publient leur code au mot près, et les maisons d'opéra leurs règlements. Ce qui suit n'est pas un conseil de style, c'est le règlement.",
     "pr_l-opera-et-le-bal_usage": "On arrive avant la fermeture des portes : l'opéra ne connaît pas le retard élégant. On n'applaudit ni entre les mouvements ni pendant un silence du chef. Dans un bal, on ne traverse pas la piste pendant une quadrille, et la révérence d'ouverture appartient aux débutants : on la regarde, on ne la mime pas.",
     "pr_les-courses_h1": "Les courses",
     "pr_les-courses_desc": "Chapeau obligatoire, ourlet sous le genou, téléphone hors de l'enceinte : le protocole de Royal Ascot, Henley et ParisLongchamp.",
     "pr_les-courses_intro": "Les courses anglaises ont mis leur étiquette par écrit, au centimètre près, et l'appliquent à la porte. Paris recommande plus qu'il n'impose. Dans les deux cas, mieux vaut connaître le texte avant de choisir sa tenue.",
     "pr_les-courses_usage": "On se renseigne sur son enclosure avant de s'habiller : chaque enceinte a son code, et l'on ne passe pas librement de l'une à l'autre. On parie avec discrétion, on gagne avec flegme. Et l'on garde ses jumelles pour la piste, pas pour les tribunes.",
     "pr_le-club-prive_h1": "Le club privé",
     "pr_le-club-prive_desc": "Pas de photos, pas d'appels, pas de pourboires : les règles publiées des clubs privés, de Mayfair à New York.",
     "pr_le-club-prive_intro": "Un club privé est une maison dont les règles sont un contrat : les House Rules sont publiées, acceptées à l'entrée, appliquées sans exception. Elles disent toutes la même chose : ce qui se passe au club reste au club.",
     "pr_le-club-prive_usage": "On ne demande jamais qui était là. On ne se présente pas soi-même à une personnalité : on attend qu'un membre fasse les présentations. On traite le personnel par son nom et avec égards. Être invité n'est pas être membre : on suit, on ne précède pas.",
     "pr_le-vernissage-et-la-foire_h1": "Le vernissage et la foire",
     "pr_le-vernissage-et-la-foire_desc": "Preview sur invitation, photos sans flash, sacs portés à la main : le protocole des foires d'art et des vernissages.",
     "pr_le-vernissage-et-la-foire_intro": "Le marché de l'art a codifié jusqu'à la taille des sacs. Les foires publient leurs conditions d'accès et leurs interdits ; le vernissage, lui, obéit à des usages que personne n'écrit. Les deux se maîtrisent.",
     "pr_le-vernissage-et-la-foire_usage": "Au vernissage, on regarde les œuvres avant de chercher les visages. On ne négocie jamais un prix à voix haute : on s'approche du stand et l'on demande la liste. On ne monopolise ni l'artiste ni le galeriste, et les points rouges se commentent en partant, pas devant l'artiste.",
     "mo_octobre-a-paris_h1": "Octobre à Paris",
     "mo_octobre-a-paris_desc": "Fashion Week, Arc de Triomphe, Journées Particulières, Art Basel Paris : le mois où Paris concentre le luxe mondial.",
     "mo_octobre-a-paris_intro": "Aucune ville ne concentre autant le calendrier du luxe qu'un mois d'octobre parisien : la Fashion Week s'achève, Longchamp couronne son champion, LVMH ouvre ses ateliers, puis le Grand Palais accueille le marché de l'art mondial, ventes du soir comprises. Voici les portes, dans l'ordre du calendrier.",
     "mo_semaine-des-joyaux-geneve_h1": "La semaine des joyaux de Genève",
     "mo_semaine-des-joyaux-geneve_desc": "Début novembre, Christie's, Sotheby's et Phillips exposent au public les plus beaux joyaux du monde avant de les vendre.",
     "mo_semaine-des-joyaux-geneve_intro": "Chaque automne, les grandes maisons de vente convergent vers le Léman : diadèmes, diamants de couleur et provenances royales s'exposent au public pendant plusieurs jours, avant de passer sous le marteau. C'est la porte la plus accessible de la haute joaillerie : les expositions des lots sont ouvertes, souvent gratuitement.",
     "mo_septembre-a-venise_h1": "Septembre à Venise",
     "mo_septembre-a-venise_desc": "La Mostra ouvre la saison des tapis rouges, l'amfAR la couronne : dix jours où Venise devient la capitale du cinéma mondial.",
     "mo_septembre-a-venise_intro": "Le premier tapis rouge de la rentrée se déroule sur le Lido : dix jours de Mostra, le gala de l'amfAR en apothéose, et une lagune entière en habits de première. Les palais d'art restent ouverts pendant le festival, et le grand bal du Carnaval se réserve déjà.",
     "mo_septembre-a-monaco_h1": "Septembre à Monaco",
     "mo_septembre-a-monaco_desc": "Le Yacht Show, le gala de la Fondation Prince Albert II et les dernières nuits du Jimmy'z : la Principauté en rentrée mondaine.",
     "mo_septembre-a-monaco_intro": "La rentrée monégasque tient en une semaine : le Yacht Show amarre les plus grands navires du monde à Port Hercule, la Fondation Prince Albert II donne son dîner de gala, et le Jimmy'z joue ses toutes dernières nuits de la saison. Une seule semaine, quatre portes.",
     "mo_le-reveillon-des-palaces_h1": "Le Réveillon des palaces",
     "mo_le-reveillon-des-palaces_desc": "De Saint-Moritz à Saint-Barth, de Marrakech à Rio : où le monde passe la nuit du 31 décembre.",
     "mo_le-reveillon-des-palaces_intro": "Une seule nuit, et une géographie entière : les galas alpins de Saint-Moritz et Gstaad, les dîners pieds dans le sable de Saint-Barth, les palais de Marrakech aux mille bougies, Dubaï et Rio en feux d'artifice. Les tables se réservent dès l'automne ; voici où elles se trouvent.",
     "mo_vienne-la-saison-des-bals_h1": "Vienne, la saison des bals",
     "mo_vienne-la-saison-des-bals_desc": "Du Concert du Nouvel An au Bal de l'Opéra : l'hiver viennois, ses tirages au sort et ses valses.",
     "mo_vienne-la-saison-des-bals_intro": "Nulle part l'hiver n'est aussi cérémonieux qu'à Vienne : le Concert du Nouvel An ouvre l'année, le Bal des Philharmoniker la poursuit, le Bal de l'Opéra la couronne. Les places s'y gagnent plus qu'elles ne s'achètent : tirages au sort, fenêtres d'inscription, quotas. Le guide des ballots explique la mécanique ; voici les dates.",
     "ville_paris": "Paris", "ville_londres": "Londres", "ville_monaco": "Monaco",
     "ville_sttropez": "Saint-Tropez & Pampelonne", "ville_riviera": "Riviera italienne & Sardaigne",
     "ville_ibiza": "Ibiza & Baléares", "ville_mykonos": "Mykonos", "ville_miami": "Miami",
     "dc": {"Tenue de soirée / robe longue": "Tenue de soirée / robe longue",
            "Chic décontracté (chapeau conseillé)": "Chic décontracté (chapeau conseillé)",
            "Black tie (tenue de soirée)": "Black tie (tenue de soirée)",
            "Élégance estivale (chapeau bienvenu)": "Élégance estivale (chapeau bienvenu)",
            "Tenue stricte (veste-cravate)": "Tenue stricte (veste-cravate)",
            "Tenue blanche exigée": "Tenue blanche exigée",
            "Chic estival (panama, chapeau)": "Chic estival (panama, chapeau)"},
    }
    # --- le Protocole (institution du 27/08/2026) : le savoir-être. Les
    # règles vivent dans .radar/protocole.json (source unique : institution,
    # document, url, extrait, verdict du contre-passage, date de consultation)
    # et sont injectées dans PFR sous les clés pr_<slug>_rN, traduisibles par
    # la même vague que le reste des pages éditoriales.
    try:
        with open(os.path.join(_RAD, "protocole.json"), encoding="utf-8") as _f:
            PROTO = json.load(_f)
    except Exception:
        PROTO = []
    for _t in PROTO:
        for _i, _r in enumerate(_t.get("regles") or []):
            PFR[f"pr_{_t['slug']}_r{_i+1}"] = _r["regle"]

    try:
        with open(os.path.join(_RAD, "pages-i18n.json"), encoding="utf-8") as _f:
            PTX = json.load(_f)
    except Exception:
        PTX = {}

    def X(lang, cle):
        v = (PTX.get(lang) or {}).get(cle)
        return v if v else PFR.get(cle, "")

    def Xdc(lang, dcfr):
        v = ((PTX.get(lang) or {}).get("dc") or {}).get(dcfr)
        return v if v else dcfr

    def hl_page(chemin):
        out = []
        for L in LANGS:
            out.append('<link rel="alternate" hreflang="%s" href="%s%s%s">' % (L, BASE, prefix(L), chemin))
        out.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (BASE, chemin))
        return "".join(out)

        for _d in _DICOS_LIEUX:
            v = _d.get(k)
            if isinstance(v, dict) and v.get(lang):
                return v[lang]
        return k

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
            title = f"{n} · {ville} | ConstanceParis7"
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
            nr = note_radar(e)
            if nr is not None:
                body.append(f"<div class=\"bc\"><a href=\"/note.html\">{diamants(nr)} {esc(UI['note'][lang])} : {nr}/100</a></div>")
            dv = date_verif(e)
            if dv:
                body.append(f"<div class=\"bc\"><a href=\"/methode.html\">✓ {esc(UI['verified'][lang])} {dv}</a></div>")
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
                nav.append(f"<a href=\"{u_place(lieu, lang)}\">{esc(UI['all_in'][lang])} · {esc(place_label(pk, lang))}</a>")
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
            list_page(place_label(k, lang), u_place(v, lang), v["events"], v, u_place)
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
            hub.append(f"<a href=\"{u_place(v, lang)}\">{esc(place_label(k, lang))} ({len(v['events'])})</a>")
        hub.append("</div>")
        if True:
            hub.append(f"<h2 class=\"sub\">{esc(X(lang,'explorer'))}</h2><div class=\"chips\">"
                + "".join(f"<a href=\"{prefix(lang)}/moments/{s}.html\">{esc(X(lang,'mo_'+s+'_h1'))}</a>"
                          for s in ("octobre-a-paris","septembre-a-venise","septembre-a-monaco",
                                    "semaine-des-joyaux-geneve","le-reveillon-des-palaces","vienne-la-saison-des-bals"))
                + f"<a href=\"{prefix(lang)}/adresses.html\">{esc(X(lang,'a_h1'))}</a>"
                + f"<a href=\"{prefix(lang)}/vestiaire.html\">{esc(X(lang,'v_h1'))}</a>"
                + f"<a href=\"{prefix(lang)}/protocole.html\">{esc(X(lang,'pr_h1'))}</a>"
                + f"<a href=\"{prefix(lang)}/methode.html\">{esc(X(lang,'m_h1'))}</a>"
                + f"<a href=\"/changements.html\">{esc(X(lang,'mem_h1'))}</a>"
                + f"<a href=\"/note.html\">{esc(UI['note'][lang])}</a></div>")
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

            home = [f"<h1>ConstanceParis7 · {esc(UI['luxury_events'][lang])}</h1>",
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
                    home.append(f"<li><div class=\"d\">{esc(e.get('d1',''))} · {esc(place_label((e.get('v') or '').strip(), lang))}</div>"
                                f"<div class=\"t\"><a href=\"{u_event(e, lang)}\">{esc(T(e, lang, 'n'))}</a></div></li>")
                home.append("</ul>")

            home.append(f"<h2 class=\"sub\">{esc(UI['by_cat'][lang])}</h2><div class=\"chips\">")
            for c, v in sorted(cats.items(), key=lambda kv: -len(kv[1]["events"])):
                home.append(f"<a href=\"{u_cat(v, lang)}\">{esc(cat_label(c, lang))} ({len(v['events'])})</a>")
            home.append(f"</div><h2 class=\"sub\">{esc(UI['by_place'][lang])}</h2><div class=\"chips\">")
            for k, v in sorted(places.items(), key=lambda kv: -len(kv[1]["events"]))[:40]:
                home.append(f"<a href=\"{u_place(v, lang)}\">{esc(place_label(k, lang))} ({len(v['events'])})</a>")
            home.append(f"</div><p><a href=\"{u_hub(lang)}\">{esc(UI['places_cats'][lang])} →</a></p>")

            # Le radar ne lit sa langue que dans localStorage — il n'existe
            # aucun paramètre d'URL. Sans cette ligne, un lecteur arrivé sur
            # /ja/ repartait en français dès qu'il cliquait vers le radar.
            home.append(f"<script>try{{localStorage.setItem('luxe_lang','{lang}')}}catch(e){{}}</script>")

            hl_home = "".join(f'<link rel="alternate" hreflang="{L}" href="{BASE}{u_home(L)}">'
                              for L in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{BASE}/">'
            write(p_home(lang), page(lang, f"ConstanceParis7 · {UI['luxury_events'][lang]}",
                                     tk('brandsub', UI['tagline'][lang])[:155],
                                     u_home(lang), "".join(home), hl_home))
            sitemap_urls.append(f"{BASE}{u_home(lang)}")

    # --- à propos / contact ------------------------------------------------
    # La page qui transforme un lecteur en partenaire : elle dit QUI tient le
    # radar et POURQUOI on peut le croire. Générée comme les autres.
    AP = """<div class="bc"><a href="/">Radar</a> · À propos</div>
<h1>À propos</h1>
<p class="meta">Le radar, et la personne qui le tient.</p>

<p>Je m'appelle <b>Constance</b>. J'habite le 7e arrondissement de Paris, celui
qui a donné son nom à ce site. Je tiens ce radar seule.</p>

<h2 class="sub">Ce qu'est ConstanceParis7</h2>
<p>Un radar des événements du luxe : galas, festivals, semaines de la mode,
haute joaillerie, grandes ventes aux enchères. <b>Plus de 400 événements</b>, publiés en
<b>13 langues</b> et remis à jour <b>chaque jour</b>.</p>
<p>La règle ne change pas : un événement n'entre dans le radar qu'accompagné de
<b>sa voie d'entrée</b>. Une date sans mode d'accès n'a pas d'utilité.</p>

<div class="box">
<h2>Méthode</h2>
<ul>
<li>Chaque information est prise <b>à sa source officielle</b>, puis <b>datée</b>.</li>
<li>Un doute n'est jamais publié comme une certitude : il est inscrit, puis
tranché à la vérification suivante.</li>
<li>Un lieu fermé ou un événement annulé est archivé avec sa preuve, jamais
effacé en silence.</li>
<li>Une erreur signalée est corrigée <b>sous 48 heures</b>, et la correction est
mentionnée.</li>
</ul>
</div>

<h2 class="sub">Origine</h2>
<p>Le site a été conçu avec mon père. <b>J'en assure seule la conduite depuis
août 2026</b> : la ligne éditoriale, les vérifications, les publications.</p>

<h2 class="sub">Travailler ensemble</h2>
<p>Maisons, palaces, hôtels, clubs, restaurants, joailliers, organisateurs :
<b>écrivez-moi</b>. J'étudie toute proposition sérieuse.</p>
<div class="box">
<h2>Une chose ne se négocie pas</h2>
<p><b>Une place dans le radar ne s'achète pas.</b> Un événement y figure parce
qu'il est vérifié, jamais parce qu'il est payé. Si un partenariat existe un
jour, il sera signalé comme tel, sur la fiche concernée.</p>
</div>

<h2 class="sub">Contact</h2>
<p><a class="cta" href="mailto:constanceparis75007@gmail.com">constanceparis75007@gmail.com</a></p>

<div class="chips"><a href="/">← Retour au radar</a><a href="/mentions-legales.html">Mentions légales</a></div>"""
    write("/a-propos.html",
          page("fr", "À propos · ConstanceParis7",
               "Le radar des événements du luxe, tenu depuis le 7e arrondissement de "
               "Paris : la méthode de vérification, la règle éditoriale, et comment "
               "proposer une collaboration.",
               "/a-propos.html", AP,
               '<link rel="alternate" hreflang="fr" href="%s/a-propos.html">' % BASE))
    sitemap_urls.append(f"{BASE}/a-propos.html")

    # --- direction de la publication : bascule datée, automatique ----------
    # Constance est née le 21/09/2008. Tant qu'elle est mineure, la loi du
    # 29 juillet 1881 impose que le directeur de la publication soit son
    # représentant légal. Le jour de ses 18 ans, elle le devient elle-même.
    # Cette page étant regénérée à chaque passe quotidienne, la bascule se
    # fait TOUTE SEULE le matin du 21/09/2026 : rien à penser, rien à cliquer.
    MAJORITE = date(2026, 9, 21)
    if date.today() >= MAJORITE:
        DIRPUB = ("La directrice de la publication est l'éditrice du site. Conformément à "
                  "l'article 6, III, 2° de la LCEN, son identité n'est pas rendue publique ; "
                  "elle a été communiquée à l'hébergeur.")
    else:
        DIRPUB = ("Le directeur de la publication est le représentant légal de l'éditrice. "
                  "Conformément à l'article 6, III, 2° de la LCEN, son identité n'est pas "
                  "rendue publique ; elle a été communiquée à l'hébergeur.")

    ML = """<div class="bc"><a href="/">Radar</a> · Mentions légales</div>
<h1>Mentions légales</h1>
<p class="meta">Dernière mise à jour : <b>26 août 2026</b></p>

<h2 class="sub">Éditrice du site</h2>
<p>Ce site est édité par une personne physique, <b>à titre non professionnel</b>.<br>
Contact : <a href="mailto:constanceparis75007@gmail.com">constanceparis75007@gmail.com</a></p>
<p>Conformément à l'article 6, III, 2° de la loi n° 2004-575 du 21 juin 2004 pour la
confiance dans l'économie numérique, l'éditrice, qui publie à titre non professionnel,
préserve son anonymat : son identité et son adresse ne sont pas rendues publiques. Les
éléments d'identification prévus par la loi ont été communiqués à l'hébergeur, qui les
tient à la disposition de l'autorité judiciaire.</p>

<h2 class="sub">Directeur de la publication</h2>
<p>__DIRPUB__</p>

<h2 class="sub">Hébergeur</h2>
<p>GitHub, Inc. · service GitHub Pages<br>
88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis<br>
<a href="https://github.com" target="_blank" rel="noopener nofollow">github.com</a></p>

<h2 class="sub">Nom de domaine</h2>
<p>constanceparis7.com, enregistré le 11 juillet 2026 auprès de <b>Gandi SAS</b>
(<a href="https://www.gandi.net" target="_blank" rel="noopener nofollow">gandi.net</a>).</p>

<div class="box">
<h2>Ce que ce site est, et ce qu'il n'est pas</h2>
<p>ConstanceParis7 recense des événements organisés par des tiers : maisons, hôtels,
festivals, musées, clubs. Le site <b>n'organise aucun événement, ne vend aucun billet,
ne perçoit aucune commission</b> et n'entretient aucun lien contractuel avec les
organisateurs cités.</p>
<p>Chaque information est vérifiée à sa source officielle, puis datée. Les dates, les
tarifs et les conditions d'accès peuvent changer sans préavis :
<b>confirmez toujours auprès de l'organisateur avant de vous déplacer ou de réserver.</b></p>
<p>Une erreur vous a échappé ? Écrivez à
<a href="mailto:constanceparis75007@gmail.com">constanceparis75007@gmail.com</a> :
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
<a href="mailto:constanceparis75007@gmail.com">constanceparis75007@gmail.com</a>. Vous pouvez
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
          page("fr", "Mentions légales · ConstanceParis7",
               "Éditrice, directrice de la publication, hébergeur, propriété "
               "intellectuelle et données personnelles du radar ConstanceParis7.",
               "/mentions-legales.html", ML.replace("__DIRPUB__", DIRPUB),
               '<link rel="alternate" hreflang="fr" href="%s/mentions-legales.html">' % BASE))
    sitemap_urls.append(f"{BASE}/mentions-legales.html")


    MOMENTS = [
     {"slug": "octobre-a-paris",
      "noms": ["Paris Fashion Week, Prêt-à-porter Printemps-Été 2027",
               "Qatar Prix de l'Arc de Triomphe 2026",
               "Les Journées Particulières LVMH 2026, 69 lieux ouverts dans 12 pays",
               "Chaumet ouvre le 12 place Vendôme, Journées Particulières LVMH",
               "Repossi ouvre le 6 place Vendôme, Journées Particulières LVMH",
               "Art Basel Paris 2026, Grand Palais",
               "Sotheby's Paris, vente du soir « Modernités » (orbite Art Basel Paris)",
               "Artcurial, vente « La Modernité en partage » (Collection Louis Grandchamp des Raux, orbite Art Basel Paris)"]},
     {"slug": "semaine-des-joyaux-geneve",
      "noms": ["Vente Sotheby's Fine Jewelry et exposition au Mandarin Oriental, Genève",
               "Phillips, The Geneva Jewels Auction VII, Hôtel Président",
               "Vente Sotheby's Royal & Noble Jewels, Genève",
               "Vente Christie's Magnificent Jewels, Genève",
               "Watches and Wonders Geneva 2027",
               "GemGenève 2027"]},
     {"slug": "septembre-a-venise",
      "noms": ["Mostra de Venise 2026, 83e Festival international du film",
               "amfAR Gala Venezia 2026, 6e édition",
               "Helter Skelter: Arthur Jafa and Richard Prince (Fondazione Prada Venise)",
               "Il Ballo del Doge 2027, bal masqué de gala du Carnaval de Venise"]},
     {"slug": "septembre-a-monaco",
      "noms": ["Monaco Yacht Show 2026",
               "MY Yacht Monaco, soirée privée à bord pendant le Monaco Yacht Show",
               "Monte-Carlo Gala for Planetary Health, dîner de gala de la Fondation Prince Albert II",
               "Jimmy'z Monte-Carlo (saison 2026)",
               "Sass Café Monte-Carlo, dîner-club des célébrités (soirées d'été)"]},
     {"slug": "le-reveillon-des-palaces",
      "noms": ["Gala du Nouvel An du Badrutt's Palace",
               "Réouverture d'hiver du Gstaad Palace et Gala du Nouvel An",
               "Réveillon d'Eden Rock, St Barths (dîner de gala et soirée dansante)",
               "Dîner de gala du Réveillon au Cheval Blanc St-Barth Isle de France",
               "Réveillon de la Saint-Sylvestre à La Mamounia",
               "Réveillon du Nouvel An au Royal Mansour Marrakech",
               "Réveillon du Nouvel An, Bulgari Resort Dubai (Yacht Club Gala & Festa di Capodanno)",
               "Réveillon do Copacabana Palace"]},
     {"slug": "vienne-la-saison-des-bals",
      "noms": ["Neujahrskonzert der Wiener Philharmoniker 2027",
               "84. Ball der Wiener Philharmoniker",
               "69. Wiener Opernball"]},
    ]
    ADRESSES = [
     ("ville_paris", ["Les Jardins de Bagatelle, Garden Club (saison estivale 2026)"]),
     ("ville_londres", ["Clubs prives Mayfair - Annabel's, 5 Hertford Street, Oswald's (Birley)"]),
     ("ville_monaco", ["Jimmy'z Monte-Carlo (saison 2026)",
                 "Sass Café Monte-Carlo, dîner-club des célébrités (soirées d'été)"]),
     ("ville_sttropez", ["Gaïo Saint-Tropez, dîner-cabaret & club 2026",
                 "Sanctum Saint-Tropez, saison club 2026",
                 "SAINT Ramatuelle, nouveau beach club d'exception (Bagatelle Group)",
                 "Beach clubs de Pampelonne, Loulou, Casa Amor, Bagatelle, Gigi : soirées d'août"]),
     ("ville_riviera", ["Covo di Nord-Est, club iconique de la Riviera",
                 "Bagni Fiore Paraggi & Langosteria Paraggi (terrasse Dior)",
                 "Phi Beach (Forte Cappellini), Saison 2026 sunset & club",
                 "Sottovento Club Porto Cervo, Saison 2026",
                 "Nammos Baja Sardinia, saison beach club 2026 (nouvelle ouverture)"]),
     ("ville_ibiza", ["Lio Ibiza, Cabaret dinner-show 'Halftime Show' & club",
                 "Blue Marlin Ibiza, Beach club VIP (Cala Jondal)",
                 "Nikki Beach Ibiza, Beach club (Santa Eulalia)"]),
     ("ville_mykonos", ["Nammos Mykonos, Legendary Beach Party (quotidien)",
                  "Principote, Beach club chic de Panormos"]),
     ("ville_miami", ["LIV at Fontainebleau, nightclub iconique (soirees d'ete)",
                "Nikki Beach Miami Beach, Amazing Sundays & Saturdance (beach club ADN Riviera)"]),
    ]
    par_nom = {e.get("n"): e for e in pages}
    par_dc = {}
    for e in pages:
        _dc = (e.get("dc") or "").strip()
        if _dc:
            par_dc.setdefault(_dc, []).append(e)
    ascot = par_nom.get("Royal Ascot 2027")
    absents_pages = set()

    for lang in LANGS:
        # ----- Méthode -----
        corps = [f"<div class=\"bc\"><a href=\"{prefix(lang)}/\">{esc(UI['radar'][lang])}</a> · {esc(X(lang,'bc_methode'))}</div>",
                 f"<h1>{esc(X(lang,'m_h1'))}</h1>",
                 f"<p class=\"meta\">{esc(X(lang,'m_meta'))}</p>",
                 f"<p>{esc(X(lang,'m_intro'))}</p>",
                 f"<div class=\"box\"><h2>{esc(X(lang,'m_rules_t'))}</h2><ul>"]
        for k in ("m_r1", "m_r2", "m_r3", "m_r4", "m_r5"):
            corps.append(f"<li>{X(lang,k)}</li>")
        corps.append(f"<li>{X(lang,'m_r6')} <a href=\"mailto:constanceparis75007@gmail.com\">{esc(X(lang,'m_signaler'))}</a>.</li></ul></div>")
        corps.append(f"<h2 class=\"sub\">{esc(X(lang,'m_badge_t'))}</h2><p>{X(lang,'m_badge_p')}</p>")
        corps.append(f"<h2 class=\"sub\">{esc(X(lang,'m_langs_t'))}</h2><p>{esc(X(lang,'m_langs_p'))}</p>")
        corps.append(f"<div class=\"chips\"><a href=\"{prefix(lang)}/\">← {esc(X(lang,'retour'))}</a><a href=\"{prefix(lang)}/a-propos.html\">À propos</a></div>"
                     if lang == "fr" else
                     f"<div class=\"chips\"><a href=\"{prefix(lang)}/\">← {esc(X(lang,'retour'))}</a></div>")
        chemin = "/methode.html"
        write(prefix(lang) + chemin, page(lang, f"{X(lang,'m_h1')} · ConstanceParis7", X(lang, "m_desc"),
              prefix(lang) + chemin, "".join(corps), hl_page(chemin)))
        sitemap_urls.append(f"{BASE}{prefix(lang)}{chemin}")

        # ----- Moments -----
        for mo in MOMENTS:
            s = mo["slug"]
            corps = [f"<div class=\"bc\"><a href=\"{prefix(lang)}/\">{esc(UI['radar'][lang])}</a> · {esc(X(lang,'bc_moments'))}</div>",
                     f"<h1>{esc(X(lang,'mo_'+s+'_h1'))}</h1>",
                     f"<p class=\"meta\">{esc(X(lang,'mo_'+s+'_intro'))}</p>", "<ul class=\"cards\">"]
            for nom in mo["noms"]:
                e = par_nom.get(nom)
                if not e:
                    absents_pages.add(nom); continue
                sw = T(e, lang, "sw") or ""
                corps.append(f"<li><div class=\"d\">{esc(T(e,lang,'dt') or e.get('d1',''))}</div>"
                             f"<a class=\"t\" href=\"{u_event(e,lang)}\">{esc(T(e,lang,'n'))}</a>"
                             + (f"<div>{esc(sw[:140])}</div>" if sw else "") + "</li>")
            corps.append("</ul>")
            if s == "vienne-la-saison-des-bals" and lang == "fr":
                corps.append("<p><a href=\"/vestiaire.html\">Le Vestiaire</a> dit comment s'y habiller ; le guide des tirages au sort, comment s'y inscrire.</p>")
            corps.append(f"<div class=\"chips\"><a href=\"{prefix(lang)}/\">← {esc(X(lang,'retour'))}</a>"
                         f"<a href=\"{u_hub(lang)}\">{esc(UI['places_cats'][lang])}</a></div>")
            chemin = f"/moments/{s}.html"
            write(prefix(lang) + chemin, page(lang, f"{X(lang,'mo_'+s+'_h1')} · ConstanceParis7",
                  X(lang, "mo_" + s + "_desc"), prefix(lang) + chemin, "".join(corps), hl_page(chemin)))
            sitemap_urls.append(f"{BASE}{prefix(lang)}{chemin}")

        # ----- Adresses -----
        corps = [f"<div class=\"bc\"><a href=\"{prefix(lang)}/\">{esc(UI['radar'][lang])}</a> · {esc(X(lang,'bc_adresses'))}</div>",
                 f"<h1>{esc(X(lang,'a_h1'))}</h1>",
                 f"<p class=\"meta\">{esc(X(lang,'a_meta'))}</p>",
                 f"<p>{esc(X(lang,'a_p1'))}</p>", f"<p>{esc(X(lang,'a_p2'))}</p>"]
        for cle_ville, noms in ADRESSES:
            corps.append(f"<h2 class=\"sub\">{esc(X(lang,cle_ville))}</h2><ul class=\"cards\">")
            for nom in noms:
                e = par_nom.get(nom)
                if not e:
                    absents_pages.add(nom); continue
                sw = T(e, lang, "sw") or ""
                corps.append(f"<li><a class=\"t\" href=\"{u_event(e,lang)}\">{esc(T(e,lang,'n'))}</a>"
                             + (f"<div>{esc(sw[:130])}</div>" if sw else "") + "</li>")
            corps.append("</ul>")
        corps.append(f"<div class=\"chips\"><a href=\"{prefix(lang)}/\">← {esc(X(lang,'retour'))}</a>"
                     f"<a href=\"{prefix(lang)}/methode.html\">{esc(X(lang,'m_h1'))}</a></div>")
        chemin = "/adresses.html"
        write(prefix(lang) + chemin, page(lang, f"{X(lang,'a_h1')} · ConstanceParis7", X(lang, "a_desc"),
              prefix(lang) + chemin, "".join(corps), hl_page(chemin)))
        sitemap_urls.append(f"{BASE}{prefix(lang)}{chemin}")

        # ----- Vestiaire -----
        corps = [f"<div class=\"bc\"><a href=\"{prefix(lang)}/\">{esc(UI['radar'][lang])}</a> · {esc(X(lang,'bc_vestiaire'))}</div>",
                 f"<h1>{esc(X(lang,'v_h1'))}</h1>",
                 f"<p class=\"meta\">{esc(X(lang,'v_meta'))}</p>",
                 f"<p>{esc(X(lang,'v_p1'))}</p>"]
        for dcfr in sorted(par_dc, key=lambda k: -len(par_dc[k])):
            evs = sorted(par_dc[dcfr], key=lambda e: e.get("d1", ""))
            corps.append(f"<h2 class=\"sub\">{esc(Xdc(lang, dcfr))}</h2><ul class=\"cards\">")
            for e in evs:
                corps.append(f"<li><div class=\"d\">{esc(e.get('d1',''))} · {esc(place_label((e.get('v') or '').strip(), lang))}</div>"
                             f"<a class=\"t\" href=\"{u_event(e,lang)}\">{esc(T(e,lang,'n'))}</a></li>")
            corps.append("</ul>")
        if ascot:
            corps.append(f"<div class=\"box\"><h2>{esc(X(lang,'v_ascot_t'))}</h2>"
                         f"<p>{esc(X(lang,'v_ascot_p'))} <a href=\"{u_event(ascot,lang)}\">{esc(T(ascot,lang,'n'))}</a>.</p></div>")
        corps.append(f"<div class=\"chips\"><a href=\"{prefix(lang)}/\">← {esc(X(lang,'retour'))}</a>"
                     f"<a href=\"{prefix(lang)}/protocole.html\">{esc(X(lang,'pr_h1'))}</a>"
                     f"<a href=\"{prefix(lang)}/methode.html\">{esc(X(lang,'m_h1'))}</a></div>")
        chemin = "/vestiaire.html"
        write(prefix(lang) + chemin, page(lang, f"{X(lang,'v_h1')} · ConstanceParis7", X(lang, "v_desc"),
              prefix(lang) + chemin, "".join(corps), hl_page(chemin)))
        sitemap_urls.append(f"{BASE}{prefix(lang)}{chemin}")

        # ----- Protocole (institution du 27/08/2026) -----
        # Le troisième pilier : le radar dit où aller, le Vestiaire quoi
        # porter, le Protocole comment se tenir. Règles publiées par les
        # institutions (contre-vérifiées, registre .radar/protocole.json)
        # + l'usage, assumé comme conseil de la maison.
        if PROTO:
            pr_liens = {
                "le-gala": [("f", "Monte-Carlo Gala for Planetary Health, dîner de gala de la Fondation Prince Albert II"),
                            ("f", "amfAR Gala Venezia 2026, 6e édition")],
                "la-vente-aux-encheres": [("p", "/moments/semaine-des-joyaux-geneve.html", "mo_semaine-des-joyaux-geneve_h1")],
                "l-opera-et-le-bal": [("p", "/moments/vienne-la-saison-des-bals.html", "mo_vienne-la-saison-des-bals_h1")],
                "les-courses": [("f", "Royal Ascot 2027"), ("f", "Qatar Prix de l'Arc de Triomphe 2026")],
                "le-club-prive": [("p", "/adresses.html", "a_h1")],
                "le-vernissage-et-la-foire": [("p", "/moments/octobre-a-paris.html", "mo_octobre-a-paris_h1")],
            }
            corps = [f"<div class=\"bc\"><a href=\"{prefix(lang)}/\">{esc(UI['radar'][lang])}</a> · {esc(X(lang,'bc_protocole'))}</div>",
                     f"<h1>{esc(X(lang,'pr_h1'))}</h1>",
                     f"<p class=\"meta\">{esc(X(lang,'pr_meta'))}</p>",
                     f"<p>{esc(X(lang,'pr_intro'))}</p>",
                     f"<div class=\"box\"><h2>{esc(X(lang,'pr_or_t'))}</h2><p>{esc(X(lang,'pr_or_p'))}</p></div>",
                     "<ul class=\"cards\">"]
            for t in PROTO:
                s = t["slug"]
                corps.append(f"<li><a class=\"t\" href=\"{prefix(lang)}/protocole/{s}.html\">{esc(X(lang,'pr_'+s+'_h1'))}</a>"
                             f"<div>{esc(X(lang,'pr_'+s+'_desc'))}</div></li>")
            corps.append("</ul>")
            corps.append(f"<div class=\"chips\"><a href=\"{prefix(lang)}/\">← {esc(X(lang,'retour'))}</a>"
                         f"<a href=\"{prefix(lang)}/vestiaire.html\">{esc(X(lang,'v_h1'))}</a>"
                         f"<a href=\"{prefix(lang)}/methode.html\">{esc(X(lang,'m_h1'))}</a></div>")
            chemin = "/protocole.html"
            write(prefix(lang) + chemin, page(lang, f"{X(lang,'pr_h1')} · ConstanceParis7", X(lang, "pr_desc"),
                  prefix(lang) + chemin, "".join(corps), hl_page(chemin)))
            sitemap_urls.append(f"{BASE}{prefix(lang)}{chemin}")

            for t in PROTO:
                s = t["slug"]
                corps = [f"<div class=\"bc\"><a href=\"{prefix(lang)}/\">{esc(UI['radar'][lang])}</a> · "
                         f"<a href=\"{prefix(lang)}/protocole.html\">{esc(X(lang,'bc_protocole'))}</a></div>",
                         f"<h1>{esc(X(lang,'pr_'+s+'_h1'))}</h1>",
                         f"<p class=\"meta\">{esc(X(lang,'pr_'+s+'_intro'))}</p>",
                         f"<div class=\"box\"><h2>{esc(X(lang,'pr_regles_t'))}</h2><ul>"]
                for i, r in enumerate(t["regles"]):
                    corps.append(f"<li><b>{esc(r['institution'])}.</b> {esc(X(lang, f'pr_{s}_r{i+1}'))}</li>")
                corps.append(f"</ul><p class=\"meta\">{esc(X(lang,'pr_verifie'))}</p></div>")
                corps.append(f"<h2 class=\"sub\">{esc(X(lang,'pr_usage_t'))}</h2><p>{esc(X(lang,'pr_'+s+'_usage'))}</p>")
                puces = []
                for lien in pr_liens.get(s, []):
                    if lien[0] == "f":
                        e = par_nom.get(lien[1])
                        if e:
                            puces.append(f"<a href=\"{u_event(e, lang)}\">{esc(T(e, lang, 'n'))}</a>")
                    else:
                        puces.append(f"<a href=\"{prefix(lang)}{lien[1]}\">{esc(X(lang, lien[2]))}</a>")
                if puces:
                    corps.append(f"<h2 class=\"sub\">{esc(X(lang,'pr_radar_t'))}</h2><div class=\"chips\">" + "".join(puces) + "</div>")
                corps.append(f"<div class=\"chips\"><a href=\"{prefix(lang)}/protocole.html\">← {esc(X(lang,'pr_h1'))}</a>"
                             f"<a href=\"{prefix(lang)}/vestiaire.html\">{esc(X(lang,'v_h1'))}</a></div>")
                chemin = f"/protocole/{s}.html"
                write(prefix(lang) + chemin, page(lang, f"{X(lang,'pr_'+s+'_h1')} · ConstanceParis7",
                      X(lang, "pr_" + s + "_desc"), prefix(lang) + chemin, "".join(corps), hl_page(chemin)))
                sitemap_urls.append(f"{BASE}{prefix(lang)}{chemin}")

    if absents_pages:
        print(f"gen_pages: AVERTISSEMENT pages éditoriales : fiches introuvables {sorted(absents_pages)}")


    # --- Page Mémoire (27/08/2026) : le registre visible. Le radar consigne
    # les dates qui bougent et les fenêtres de réservation ; cette page montre
    # les 14 derniers jours. Chaque année qui passe rend ce registre plus
    # précieux : personne ne peut racheter le temps.
    MEM = []
    try:
        with open(os.path.join(_RAD, "memoire.ndjson"), encoding="utf-8") as _f:
            for _l in _f:
                _l = _l.strip()
                if _l:
                    try:
                        MEM.append(json.loads(_l))
                    except Exception:
                        pass
    except Exception:
        pass
    if MEM:
        from datetime import timedelta
        _seuil = (date.today() - timedelta(days=14)).isoformat()
        chg = [m for m in MEM if m.get("type") == "changement_date" and m.get("date", "") >= _seuil]
        fen = [m for m in MEM if m.get("type") in ("fenetre_annoncee", "fenetre_ouverte", "complet")]
        obs = [m for m in MEM if m.get("type") == "observation" and m.get("date", "") >= _seuil]
        corps = ["<div class=\"bc\"><a href=\"/\">Radar</a> · Mémoire</div>",
                 "<h1>La mémoire du radar</h1>",
                 "<p class=\"meta\">Les dates qui bougent, les fenêtres qui ouvrent, les salles qui se remplissent : le radar consigne ce que le temps enseigne, et le montre.</p>",
                 "<p>Une information de luxe a une propriété que peu de sites mesurent : elle change. Une saison se prolonge, une billetterie ouvre, une salle part en deux heures. Ce registre garde la trace de ces mouvements, semaine après semaine ; d'année en année, il apprend au radar quand il faut réserver.</p>"]
        if fen:
            corps.append("<h2 class=\"sub\">Les fenêtres sous surveillance</h2><ul class=\"cards\">")
            for m in sorted(fen, key=lambda x: x.get("date", ""), reverse=True):
                e = par_nom.get(m.get("evenement"))
                lien = (f"<a class=\"t\" href=\"{u_event(e,'fr')}\">{esc(m['evenement'])}</a>" if e
                        else f"<span class=\"t\">{esc(m.get('evenement',''))}</span>")
                corps.append(f"<li><div class=\"d\">consigné le {esc(m.get('date',''))}</div>{lien}"
                             f"<div>{esc(m.get('detail',''))}</div></li>")
            corps.append("</ul>")
        if chg:
            corps.append(f"<h2 class=\"sub\">Les dates qui ont bougé (14 derniers jours)</h2><ul class=\"cards\">")
            for m in sorted(chg, key=lambda x: x.get("date", ""), reverse=True)[:30]:
                e = par_nom.get(m.get("evenement"))
                lien = (f"<a class=\"t\" href=\"{u_event(e,'fr')}\">{esc(m['evenement'])}</a>" if e
                        else f"<span class=\"t\">{esc(m.get('evenement',''))}</span>")
                corps.append(f"<li><div class=\"d\">{esc(m.get('date',''))}</div>{lien}"
                             f"<div>{esc(m.get('detail',''))}</div></li>")
            corps.append("</ul>")
        if obs:
            corps.append("<h2 class=\"sub\">Observations</h2><ul class=\"cards\">")
            for m in sorted(obs, key=lambda x: x.get("date", ""), reverse=True):
                e = par_nom.get(m.get("evenement"))
                lien = (f"<a class=\"t\" href=\"{u_event(e,'fr')}\">{esc(m['evenement'])}</a>" if e
                        else f"<span class=\"t\">{esc(m.get('evenement',''))}</span>")
                corps.append(f"<li><div class=\"d\">{esc(m.get('date',''))}</div>{lien}"
                             f"<div>{esc(m.get('detail',''))}</div></li>")
            corps.append("</ul>")
        corps.append("<p class=\"meta\">Chaque entrée porte sa preuve au registre. Les corrections du site restent par ailleurs archivées, rien ne s'efface en silence : c'est la <a href=\"/methode.html\">méthode</a>.</p>")
        corps.append("<div class=\"chips\"><a href=\"/\">← Retour au radar</a><a href=\"/methode.html\">La méthode</a></div>")
        write("/changements.html", page("fr", "La mémoire du radar · ConstanceParis7",
              "Les dates qui bougent, les billetteries qui ouvrent, les salles qui se remplissent : le registre vivant du radar.",
              "/changements.html", "".join(corps),
              '<link rel="alternate" hreflang="fr" href="%s/changements.html">' % BASE))
        sitemap_urls.append(f"{BASE}/changements.html")

    # --- la Note du radar : le barème public (institution du 27/08/2026) ---
    # La note existait depuis l'origine, en coulisses du Classement Prestige.
    # Ici elle sort de l'ombre : sceau sur chaque fiche, barème publié.
    notes = sorted(((note_radar(e), e) for e in pages if note_radar(e) is not None),
                   key=lambda t: -t[0])
    def _evenement_date(e):
        """Vrai événement daté (pour la vitrine « du moment ») : pas fini,
        et pas une fiche à l'année dont la proximité de date vaut toujours
        le maximum, sinon la vitrine ne bougerait jamais."""
        try:
            d1, d2 = date.fromisoformat(str(e.get("d1"))), date.fromisoformat(str(e.get("d2")))
        except (TypeError, ValueError):
            return False
        return d2 >= date.fromisoformat(TODAY) and (d2 - d1).days <= 90
    vitrine = [(nr, e) for nr, e in notes if _evenement_date(e)][:3]
    if notes:
        corps = ["<div class=\"bc\"><a href=\"/\">Radar</a> · La Note</div>",
                 "<h1>La Note du radar</h1>",
                 "<p class=\"meta\">Chaque événement du radar porte une note sur 100. Voici le barème, publié en entier : ce que la note mesure, et ce qu'elle ne prétend pas mesurer.</p>",
                 "<p>Un restaurant a ses étoiles, un palace a son classement. Les événements n'avaient rien : la Note du radar comble ce vide. Elle mesure l'engouement autour d'un événement : la difficulté d'y entrer, qui s'y montre, où il se tient, et à quel point c'est maintenant.</p>",
                 "<h2 class=\"sub\">On note la porte, pas la fête</h2>",
                 "<p>La Note ne juge pas si une soirée fut réussie : personne ne peut le savoir sans y avoir été, et le radar ne prétend jamais savoir ce qu'il n'a pas vérifié. Elle mesure ce qui se documente : ce qu'un événement exige, publie et promet. C'est le principe des agences de notation : lire les faits. Le ressenti, lui, n'entre pas dans la formule.</p>",
                 "<h2 class=\"sub\">Quatre critères, des poids assumés</h2>",
                 "<ul>",
                 "<li><b>L'exclusivité de l'accès (poids 4).</b> Billetterie ouverte à tous, invitation seule, liste tenue par la maison : la sélection à l'entrée, les prix publiés, la jauge.</li>",
                 "<li><b>Les personnalités attendues (poids 3).</b> Qui vient, qui organise, qui parraine, d'après les éditions précédentes documentées.</li>",
                 "<li><b>Le lieu (poids 2).</b> Un palace centenaire, un hôtel particulier fermé au public, une plage privatisée : le standing d'un lieu est un fait.</li>",
                 "<li><b>La proximité de la date (poids 1).</b> Un événement en cours vaut le maximum ; un événement lointain attend son heure. Ce critère est recalculé à chaque mise à jour du site : la Note respire avec le calendrier.</li>",
                 "</ul>",
                 "<p>La somme pondérée fait la Note, sur 100. Le Classement Prestige de l'accueil ordonne tous les événements selon cette même note : une seule formule, du haut en bas du site.</p>",
                 "<h2 class=\"sub\">Les diamants</h2>",
                 "<p>La note se lit aussi en diamants : ✦✦✦✦✦ à partir de 88, ✦✦✦✦ à partir de 76, ✦✦✦ à partir de 62, ✦✦ à partir de 48, ✦ en dessous.</p>",
                 f"<h2 class=\"sub\">Aujourd'hui sur le radar</h2>",
                 f"<p>{len(notes)} événements notés. Les plus hautes notes du moment :</p>",
                 "<ul class=\"cards\">"]
        for nr, e in vitrine:
            corps.append(f"<li><div class=\"d\">{diamants(nr)} {nr}/100</div>"
                         f"<a class=\"t\" href=\"{u_event(e,'fr')}\">{esc(e.get('n',''))}</a></li>")
        corps.append("</ul>")
        corps.append("<h2 class=\"sub\">Ce que la Note apprendra encore</h2>")
        corps.append("<p>La <a href=\"/changements.html\">Mémoire du radar</a> consigne les fenêtres de réservation et les épuisements constatés. « Complet en deux heures » est une mesure d'engouement qu'aucune formule ne remplace : d'année en année, ces relevés viendront affiner le critère d'accès. Et lorsque la rédaction franchit elle-même les portes, la fiche portera la mention « vécu et vérifié sur place ».</p>")
        corps.append("<p class=\"meta\">La façon dont chaque information est vérifiée est publiée : c'est la <a href=\"/methode.html\">méthode</a>.</p>")
        corps.append("<div class=\"chips\"><a href=\"/\">← Retour au radar</a><a href=\"/methode.html\">La méthode</a><a href=\"/changements.html\">La mémoire</a></div>")
        write("/note.html", page("fr", "La Note du radar · ConstanceParis7",
              "Le barème public de la Note du radar : quatre critères documentés, l'accès, les personnalités, le lieu, la date. On note la porte, pas la fête.",
              "/note.html", "".join(corps),
              '<link rel="alternate" hreflang="fr" href="%s/note.html">' % BASE))
        sitemap_urls.append(f"{BASE}/note.html")

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
