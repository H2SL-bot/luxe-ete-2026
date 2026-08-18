"""Récupère une recherche terminée et écrit l'atelier de vérification correspondant.
   usage : preparer_verif.py <wf_recherche> <sej|inv> <nom_atelier>"""
import json,os,re,sys
BASE="/Users/geraldlefebvre/.claude/projects/-Users-geraldlefebvre/2de0cd85-85f8-41f3-aca5-7906e9758743/subagents/workflows"
S="/private/tmp/claude-501/-Users-geraldlefebvre/2de0cd85-85f8-41f3-aca5-7906e9758743/scratchpad"
os.makedirs(S,exist_ok=True); os.chdir("/Users/geraldlefebvre/luxe-ete-2026")
wf,kind,nom=sys.argv[1],sys.argv[2],sys.argv[3]
champ="sej" if kind=="sej" else "iv"
def denorm(n):
    """Le nom lu dans le JSONL est encore échappé : \\" et \\\\ doivent être rendus,
    sinon une fiche dont le titre contient des guillemets ne retrouve jamais son entrée."""
    return n.replace('\\"','"').replace("\\\\","\\")
doc=open("index-full.html",encoding="utf-8").read()
d=json.loads(re.search(r'id="data">(.*?)</script>',doc,re.S).group(1).replace("<\\/","</"))
idx={}
for e in d: idx.setdefault(e.get("n",""),e)
cibles=[];vus=set();rejets=[]
# Fiches déjà confiées à un contrôleur ENCORE ACTIF, POUR LE MÊME CHAMP : on ne les
# redonne pas. Le 12/08/2026, ce filtre était bien trop large — il excluait toute fiche
# jamais touchée par un contrôleur, même terminé depuis des heures et même travaillant
# sur l'autre champ. Huit brouillons de séjour sur douze étaient jetés en silence.
import glob as _g, time as _t
CONF=os.path.expanduser("~/.radar-session/verificateurs")
if os.path.exists(CONF):
    for _l in open(CONF,encoding="utf-8"):
        _p=_l.split()
        if len(_p)<2 or _p[0]==wf: continue
        if _p[1]!=("sejour_corrige" if kind=="sej" else "iv_corrige"): continue   # autre champ
        for _f in _g.glob(f"{BASE}/{_p[0]}/agent-*.jsonl"):
            if _t.time()-os.path.getmtime(_f) > 1800: continue                     # terminé
            _m=re.search(r'EVENEMENT\s*:\s*(.+?)\\n',open(_f,encoding="utf-8").read(3000))
            if _m: vus.add(denorm(_m.group(1).strip()))
for l in open(f"{BASE}/{wf}/journal.jsonl",encoding="utf-8"):
    try: j=json.loads(l)
    except Exception: continue
    if j.get("type")!="result" or not isinstance(j.get("result"),dict): continue
    f=f"{BASE}/{wf}/agent-{j['agentId']}.jsonl"
    if not os.path.exists(f): continue
    head=open(f,encoding="utf-8").read(3000)
    mn=re.search(r'EVENEMENT\s*:\s*(.+?)\\n',head)
    if not mn: continue
    n=denorm(mn.group(1).strip()); e=idx.get(n) or idx.get(n.replace("&","&amp;"))
    if e is None: rejets.append(("hors index",n)); continue
    if e.get(champ): rejets.append(("deja rempli",n)); continue
    if n in vus: rejets.append(("controleur actif",n)); continue
    vus.add(n)
    cibles.append({"cle":f"{e.get('d1','')}|{e.get('n','')}","nom":e.get("n",""),
                   "ville":e.get("v",""),"lieu":e.get("l",""),"r":j["result"]})
# GARDE-FOU : ne jamais préparer la vérification d'un atelier de recherche encore en
# cours. Le 12/08/2026, préparé trente secondes trop tôt, il manquait le dernier
# chercheur : une fiche composée n'a jamais été vérifiée ni publiée, sans un mot.
import time as _tt
_actifs=[_f for _f in _g.glob(f"{BASE}/{wf}/agent-*.jsonl") if _tt.time()-os.path.getmtime(_f) < 90]
if _actifs:
    print(f"ATTENTION : {len(_actifs)} chercheur(s) de {wf} ont ecrit il y a moins de 90 s —")
    print("            l atelier de recherche n est probablement PAS termine.")
    print("            Relancez ce preparateur quand la notification de fin sera arrivee,")
    print("            sinon les derniers brouillons seront perdus en silence.")

emb=json.dumps(json.dumps(cibles,ensure_ascii=False))
SEJ='''export const meta = { name: '@N@', description: 'Verifier @C@ sejours', phases: [{ title: 'Verifier' }] }
const ITEM={type:'object',properties:{n:{type:'string'},d:{type:'string'},u:{type:'string'}},required:['n','d','u']};
const SJ={type:'object',properties:{pitch:{type:'string'},hotels:{type:'array',items:ITEM},tables:{type:'array',items:ITEM},exp:{type:'array',items:ITEM}},required:['pitch','hotels','tables','exp']};
const V={type:'object',properties:{fiable:{type:'boolean'},sejour_corrige:SJ,changements:{type:'array',items:{type:'object',properties:{element:{type:'string'},probleme:{type:'string'},action:{type:'string'}},required:['element','probleme','action']}}},required:['fiable','sejour_corrige','changements']};
const A=JSON.parse(@D@);
const out=await parallel(A.map(a=>()=>agent(
`VERIFICATION ADVERSARIALE d un sejour cle en main du site de luxe ConstanceParis7.

EVENEMENT : ${a.nom}
Ville : ${a.ville} — Lieu : ${a.lieu}

SEJOUR PROPOSE (a verifier ligne par ligne) :
${JSON.stringify(a.r,null,1)}

VOTRE MISSION : chercher a REFUTER chaque affirmation, sur le web, maintenant.
AVANT TOUT : le LIEU DE L EVENEMENT lui-meme est-il ouvert a la date annoncee ?
Un hotel ferme pour travaux, un club ferme definitivement, une saison terminee rendent
l evenement IMPOSSIBLE : dans ce cas fiable=false, et dites-le explicitement dans changements.
Puis, pour CHAQUE hotel, table et experience :
- l etablissement existe-t-il encore, et est-il OUVERT a cette date ?
- l URL est-elle vivante et OFFICIELLE (pas un agregateur, pas une page morte) ?
- etoiles Michelin, nom du chef, nombre de chambres : confirmes par une source de premiere main ?
- la distance ou la situation annoncee est-elle geographiquement vraie ?
- le pitch decrit-il bien CET evenement, sans detail invente ?

LANGUE : le site s adresse a un public francophone. Le pitch et TOUTES les descriptions
doivent etre integralement en FRANCAIS elegant. Si une phrase ou un fragment est en anglais
(ou dans une autre langue), reecrivez-le en francais dans sejour_corrige et signalez-le dans
changements. Les noms propres d etablissements restent evidemment dans leur langue.

REGLE D OR : au moindre doute, on retire. Un element supprime vaut mieux qu un element faux.
Rendez sejour_corrige complet (pitch + jusqu a 2 hotels, 2 tables, 2 experiences) et listez
dans changements TOUT ce que vous avez corrige ou supprime, avec le motif.`,
{label:`v:${a.nom.slice(0,26)}`,phase:'Verifier',schema:V}
).then(r=>({cle:a.cle,nom:a.nom,v:r})).catch(()=>null)));
return { sejours: out.filter(Boolean) }
'''
INV='''export const meta = { name: '@N@', description: 'Verifier @C@ voies d invitation', phases: [{ title: 'Verifier' }] }
const C={type:'object',properties:{t:{type:'string'},v:{type:'string'}},required:['t','v']};
const IV={type:'object',properties:{o:{type:'string'},g:{type:'string'},w:{type:'string'},c:{type:'array',items:C},trouve:{type:'boolean'}},required:['o','g','w','c','trouve']};
const V={type:'object',properties:{iv_corrige:IV,retires:{type:'array',items:{type:'object',properties:{element:{type:'string'},motif:{type:'string'}},required:['element','motif']}}},required:['iv_corrige','retires']};
const A=JSON.parse(@D@);
const out=await parallel(A.map(a=>()=>agent(
`VERIFICATION ADVERSARIALE d une voie d invitation du site ConstanceParis7.
Le site veut devenir LA reference mondiale des invitations jet-set : une seule coordonnee
fausse detruit cette credibilite.

EVENEMENT : ${a.nom}
Ville : ${a.ville} — Lieu : ${a.lieu}

VOIE D INVITATION PROPOSEE (a verifier ligne par ligne) :
${JSON.stringify(a.r,null,1)}

VOTRE MISSION : chercher a REFUTER, sur le web, maintenant.
AVANT TOUT : le lieu est-il ouvert et l evenement peut-il avoir lieu a cette date ?
Si le lieu est ferme pour travaux ou definitivement, dites-le en tete de o : c est
plus important que toute coordonnee.
Puis, pour CHAQUE coordonnee (nom, fonction, email, telephone, mobile, URL) :
- la personne existe-t-elle et occupe-t-elle ENCORE cette fonction ? (quelle source, de quand ?)
- l email est-il publie par une source officielle de premiere main, ou devine ?
- le numero est-il publie noir sur blanc par une source vivante ? Un MOBILE personnel
  non recoupe se RETIRE, toujours.
- l URL repond-elle vraiment (pas 403, pas 404, pas domaine mort, pas sous-domaine inexistant) ?
- l acces gratuit annonce est-il reellement decrit par l organisateur, ou extrapole ?
- tarif, regle d acces, date : confirmes a la source ?

REGLE D OR : tout ce qui n est pas prouve aujourd hui est retire, ou explicitement date
comme piste historique. Rendez iv_corrige complet et listez dans retires TOUT element
supprime avec son motif precis.`,
{label:`i:${a.nom.slice(0,26)}`,phase:'Verifier',schema:V}
).then(r=>({cle:a.cle,nom:a.nom,v:r})).catch(()=>null)));
return { invitations: out.filter(Boolean) }
'''
tpl=(SEJ if kind=="sej" else INV).replace("@N@",nom).replace("@C@",str(len(cibles))).replace("@D@",emb)
p=f"{S}/{nom}.js"; open(p,"w",encoding="utf-8").write(tpl)
print(f"{nom} : {len(cibles)} fiches à vérifier → {p}")
if rejets:
    print(f"   {len(rejets)} brouillon(s) NON transmis :")
    for _r,_n in rejets: print(f"     · [{_r}] {_n[:62]}")
