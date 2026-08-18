import json,os,re
BASE="/Users/geraldlefebvre/.claude/projects/-Users-geraldlefebvre/2de0cd85-85f8-41f3-aca5-7906e9758743/subagents/workflows"
os.chdir("/Users/geraldlefebvre/luxe-ete-2026")

# Le registre des ateliers de vérification était tenu À LA MAIN. Le 12/08/2026, y avoir
# inscrit les identifiants des ateliers de RECHERCHE au lieu de ceux de VÉRIFICATION a
# fait répondre « rien de neuf » au collecteur pendant que seize fiches vérifiées
# attendaient, invisibles. Une liste que l'on peut oublier de tenir finira par être
# oubliée : on ne tient plus de liste, on balaye tout.
#
# Un atelier est un atelier de vérification si son journal contient un résultat portant
# `sejour_corrige` ou `iv_corrige` — c'est la signature du schéma de sortie, elle ne
# peut pas mentir. Le fichier ~/.radar-session/verificateurs n'est plus lu que pour
# mémoire humaine ; il n'a plus aucun effet sur ce qui est récolté.
WF=[]
import glob as _glob
for _jp in sorted(_glob.glob(f"{BASE}/wf_*/journal.jsonl")):
    _wf=os.path.basename(os.path.dirname(_jp))
    _champs=set()
    try:
        for _l in open(_jp,encoding="utf-8"):
            for _c in ("sejour_corrige","iv_corrige"):
                if f'"{_c}"' in _l: _champs.add(_c)
            if len(_champs)==2: break
    except Exception:
        continue
    for _c in sorted(_champs):
        WF.append((_wf,_c))

doc=open("index-full.html",encoding="utf-8").read()
m=re.search(r'(<script type="application/json" id="data">)(.*?)(</script>)',doc,re.S)
data=json.loads(m.group(2).replace("<\\/","</"))
idx={}
for e in data:
    idx.setdefault(e.get("n",""),e)
ns=ni=0; fermes=[]; brides=[]
for wf,champ in WF:
    jp=f"{BASE}/{wf}/journal.jsonl"
    if not os.path.exists(jp): continue
    for l in open(jp,encoding="utf-8"):
        try: j=json.loads(l)
        except Exception: continue
        r=j.get("result")
        if j.get("type")!="result" or not isinstance(r,dict) or champ not in r: continue
        f=f"{BASE}/{wf}/agent-{j['agentId']}.jsonl"
        if not os.path.exists(f): continue
        head=open(f,encoding="utf-8").read(3000)
        mn=re.search(r'EVENEMENT\s*:\s*(.+?)\\n',head)
        if not mn: continue
        # Un vérificateur privé de recherche web ne voit que ce qu'on lui montre :
        # il peut confirmer une page officielle, pas découvrir une source qui contredit.
        # On publie son travail, mais la fiche part au ré-audit (règle du 11/08/2026).
        bride = "web search budget" in open(f,encoding="utf-8").read()
        # Le nom lu dans le JSONL est encore ÉCHAPPÉ : une fiche dont le titre porte
        # des guillemets — « La Lanterne d\'Hermès (theme \\"L\'appel du large\\") » — ne
        # retrouvait jamais son entrée et disparaissait sans un mot. Bug corrigé dans
        # preparer_verif.py le 18/08/2026 au matin, mais pas ici : il a fallu qu\'une
        # fiche sur douze soit récoltée pour que ça se voie.
        nom=mn.group(1).strip().replace('\\"','"').replace("\\\\","\\")
        e=idx.get(nom) or idx.get(nom.replace("&","&amp;"))
        if e is None: continue
        if champ=="sejour_corrige":
            if e.get("sej"): continue
            # Les ateliers de REPRISE (18/08/2026) rendent « reel » au lieu de
            # « fiable » : même sens, autre nom. Sans cette équivalence, dix-sept
            # séjours vérifiés partaient au rejet en silence.
            fiable = r.get("fiable", r.get("reel"))
            if not fiable:
                fermes.append(nom); continue
            s=r["sejour_corrige"]
            if not s.get("pitch"): continue
            e["sej"]={"base":(e.get("v") or "")+(f" — autour de {e.get('l')}" if e.get("l") else ""),
                      "pitch":s["pitch"],"hotels":s.get("hotels",[])[:2],
                      "tables":s.get("tables",[])[:2],"exp":s.get("exp",[])[:2]}
            ns+=1
            if bride: brides.append(nom)
        else:
            if e.get("iv"): continue
            iv=r["iv_corrige"]
            if not (iv.get("o") or iv.get("w")): continue
            e["iv"]={"o":iv.get("o",""),"g":iv.get("g",""),"w":iv.get("w",""),"c":iv.get("c",[])[:14]}
            ni+=1
            if bride: brides.append(nom)
if ns or ni:
    body=json.dumps(data,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    open("index-full.html","w",encoding="utf-8").write(doc[:m.start(2)]+body+doc[m.end(2):])
print(f"SEJ={ns} INV={ni}")
if brides:
    RA="/Users/geraldlefebvre/luxe-ete-2026/.radar/a-reverifier.md"
    import datetime
    jour=datetime.date.today().strftime("%d/%m/%Y")
    with open(RA,"a",encoding="utf-8") as fh:
        fh.write("\n## Vérifiées à moyens réduits — ré-audit obligatoire\n\n")
        fh.write("Vérificateur privé de recherche web (budget de session épuisé) : il a pu\n")
        fh.write("contrôler les pages officielles mais pas découvrir une source contredisante.\n\n")
        for n in sorted(set(brides)):
            fh.write(f"- [ ] {n} — inscrit le {jour}\n")
    print(f"⚠️ {len(set(brides))} fiche(s) inscrites au ré-audit dans .radar/a-reverifier.md")
if fermes:
    # ne re-signaler que les rejets pas encore traités (un rejet examiné une fois
    # est noté dans ~/.radar-session/rejets-traites, sinon il crie à chaque tour)
    T=os.path.expanduser("~/.radar-session/rejets-traites")
    vus=set(open(T,encoding="utf-8").read().splitlines()) if os.path.exists(T) else set()
    neufs=[n for n in fermes if n not in vus]
    if neufs:
        print("⚠️ REJETÉS (à examiner — lieu fermé ou événement impossible) :")
        for n in neufs: print("   ·",n[:70])
