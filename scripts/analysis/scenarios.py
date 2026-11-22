"""Sensitivity scenarios for the 1.0.0 headline (appendix only).

Each scenario copies index/method.v1.0.json, changes one choice, and runs the
v1.0 compiler on the copy in a temporary directory. index/computed.v1.0.json is
never written. About 3-4 minutes (20,000 draws per scenario).
"""
import json, copy, sys, tempfile, importlib
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(REPO/'scripts'))
import compute_index as ci
base=json.load(open(REPO/'index/method.v1.0.json'))
def run(name, mutate):
    m=copy.deepcopy(base)
    try:
        mutate(m)
    except (ValueError, KeyError) as exc:  # scenario assumes rc.2 structure (K1 in Block A)
        print(f"{name:42s} n/a under the current method ({exc!r})", flush=True)
        return None
    p=Path(tempfile.mkdtemp())/'m.json'; p.write_text(json.dumps(m))
    c=ci.compute(method_path=p)
    out={}
    for pop in ('EU27','FI'):
        b=c['populations'][pop]; h=b['headline']
        pil={x['id']:x for x in b['pillars']}
        out[pop]=dict(H=h.get('score'),lo=h.get('p2_5'),hi=h.get('p97_5'),G=h.get('geometric_mean'),status=h['status'],w=h.get('weights'),
                      dep=pil['deployment']['score'],cap=pil['capital_intensity']['score'],cap_status=pil['capital_intensity']['status'],
                      vd=(h.get('variance_decomposition') or {}).get('share_data_pct'),vw=(h.get('variance_decomposition') or {}).get('share_weights_pct'))
    print(f"{name:42s} EU27 {out['EU27']['H']} [{out['EU27']['lo']}–{out['EU27']['hi']}] G {out['EU27']['G']} {out['EU27']['status']} dep {out['EU27']['dep']} cap {out['EU27']['cap']} | FI {out['FI']['H']} [{out['FI']['lo']}–{out['FI']['hi']}] G {out['FI']['G']} {out['FI']['status']} dep {out['FI']['dep']} cap {out['FI']['cap']}",flush=True)
    return out
def pillar(m,pid): return [p for p in m['pillars'] if p['id']==pid][0]
def ind(m,iid):
    for p in m['pillars']:
        for i in p['indicators']:
            if i['id']==iid: return i
R={}
R['baseline']=run('baseline',lambda m:None)
def a(m):
    m['block_a']['pillars'].remove('capital_intensity'); m['block_a']['nominal_weights'].pop('capital_intensity'); pillar(m,'capital_intensity')['block']='B_conditions'
R['a_K1_to_blockB']=run('(a) K1 -> Block B (min 2 pillars kept)',a)
def c(m):
    a(m); m['evidence_rules']['headline']['min_eligible_block_a_pillars']=1
R['c_deployment_only']=run('(a)+(c) deployment alone (min 1 pillar)',c)
def b25(m):
    m['block_a']['nominal_weights'].update(deployment=0.75,cost_to_serve=0.75,capital_intensity=0.5)
R['b_cap_weight_0.4']=run('(b-var) capital nominal 0.5 vs 0.75 (eff 0.4)',b25)
def b4(m):
    m['block_a']['nominal_weights'].update(deployment=0.75,cost_to_serve=0.75,capital_intensity=0.25)
R['b_cap_weight_0.25']=run('(b-var) capital eff weight 0.25',b4)
for wd in (0.25,0.75,1.0):
    def f(m,wd=wd): m['scoring']['within_pillar_aggregation']['channel_weights'].update(digital=wd,physical=round(1-wd,4))
    R[f'channel_digital_{wd}']=run(f'channel weights digital {wd}',f)
def ceil80(m):
    for i in ('D1_ent_any_ai','D2_ind_genai','D3_ent_depth_ge3','D4_ent_autonomous'): ind(m,i)['ceiling']=80.0
R['ceiling_80']=run('D1-D4 ceiling 80 %',ceil80)
def d4(m): ind(m,'D4_ent_autonomous')['ceiling']=round(1.7*4.38,2)
R['d4_ceiling_1.7xDK']=run('D4 ceiling 1.7 x best MS (DK 4.38 -> 7.45)',d4)
for k in (10.0,20.0):
    def f(m,k=k): ind(m,'K1_gfcf_ict_ipp_gdp')['ceiling']=k
    R[f'k1_ceiling_{k}']=run(f'K1 ceiling {k}',f)
print(json.dumps(R, indent=1)) if '--json' in sys.argv else None
