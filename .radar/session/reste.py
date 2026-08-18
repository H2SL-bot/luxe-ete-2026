import json,re,os
os.chdir("/Users/geraldlefebvre/luxe-ete-2026")
doc=open("index-full.html",encoding="utf-8").read()
m=re.search(r'id="data">(.*?)</script>',doc,re.S)
d=json.loads(m.group(1).replace("<\\/","</"))
T=len(d); ns=sum(1 for e in d if e.get("sej")); ni=sum(1 for e in d if e.get("iv"))
def bar(n,t,lab):
    f=int(24*n/t); print(f"  {lab:<24} {'█'*f}{'░'*(24-f)} {n}/{t}   reste {t-n}")
bar(T,T,"1. traductions 13 langues"); bar(ns,T,"2. séjours clé en main"); bar(ni,T,"3. voies d'invitation")
