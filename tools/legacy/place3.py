import numpy as np, os, json, math
from PIL import Image
from scipy import ndimage
Image.MAX_IMAGE_PIXELS=None
SP=os.path.dirname(os.path.abspath(__file__))
W=os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
N=8192; HALF=4096; B=4; NB=N//B; BUF=8; BB=BUF//B      # 2 blocks of clearance

h=np.load(os.path.join(SP,"h.npy")); occ=np.load(os.path.join(SP,"occ.npy"))
hb=h.reshape(NB,B,NB,B); hmax=hb.max(axis=(1,3)); hmin=hb.min(axis=(1,3)); del hb
occb=occ.reshape(NB,B,NB,B).any(axis=(1,3))
sp=np.array(Image.open(os.path.join(W,"splat3.png")))
roadb=((sp[...,0]>100)|(sp[...,1]>100)).reshape(NB,B,NB,B).any(axis=(1,3)); del sp
m=48//B; occb[:m,:]=occb[-m:,:]=occb[:,:m]=occb[:,-m:]=True
for x,z in [(3136,-1266),(2235,149),(2869,-182),(2227,-169),(-2587,-353),(-2740,-30),
            (-2445,-219),(-2209,-125),(1310,1171),(3638,-2602)]:
    a,b_=(z+HALF)//B,(x+HALF)//B; occb[max(0,a-15):a+15, max(0,b_-15):b_+15]=True
st=ndimage.generate_binary_structure(2,2)
NEAR={40:ndimage.binary_dilation(roadb,st,iterations=10),
      90:ndimage.binary_dilation(roadb,st,iterations=22),
      200:ndimage.binary_dilation(roadb,st,iterations=50)}
bio=np.array(Image.open(os.path.join(W,"biomes.png")))[::B,::B]
BIOC={(255,168,0):"burnt_forest",(255,228,119):"desert",(0,64,0):"pine_forest",
      (255,255,255):"snow",(186,0,255):"wasteland"}
bkey=(bio[...,0].astype(np.uint32)<<16)|(bio[...,1].astype(np.uint32)<<8)|bio[...,2]; del bio
bname=np.zeros((NB,NB),np.uint8); NAMES=["other"]
for i,(c,n) in enumerate(BIOC.items(),1):
    NAMES.append(n); bname[bkey==((c[0]<<16)|(c[1]<<8)|c[2])]=i
del bkey

def fwd(arr, nz, nx, op, cval, back=0):
    """window anchored so that index i covers [i-back, i-back+n-1] in each axis"""
    return op(arr, size=(nz,nx), mode='constant', cval=cval,
              origin=(-((nz-1)//2)+back, -((nx-1)//2)+back))

geom={}
def geo(w,d):
    if (w,d) in geom: return geom[(w,d)]
    ob=int(math.ceil((w+2*BUF)/B)); od=int(math.ceil((d+2*BUF)/B))     # footprint + clearance
    fw=int(math.ceil(w/B)); fd=int(math.ceil(d/B))                     # bare footprint
    o =fwd(occb.astype(np.uint8), od, ob, ndimage.maximum_filter, 1, back=BB)
    hx=fwd(hmax, fd, fw, ndimage.maximum_filter,  1e4)
    hn=fwd(hmin, fd, fw, ndimage.minimum_filter, -1e4)
    geom[(w,d)]=(o==0, hx-hn, hn, (fd,fw)); return geom[(w,d)]

TIERS=[(1.6,40,220),(2.5,40,180),(3.5,90,140),(5.0,200,110),(7.0,None,80)]
inv=json.load(open(os.path.join(SP,"inv.json")))
EXC=("_ocean_","stilt","swamp_market","bridgehouse","quarry_house")
def skip(r):
    n=r["name"].lower(); t=(r.get("Tags") or "").lower()
    if "part" in [x.strip() for x in t.split(",")] or n.startswith(("part_","rwg_tile","tile_")): return "part / not standalone"
    if "catalog" in n or "showroom" in n or "area_rugs" in n: return "showroom / not a POI"
    if r["mod"]=="AAE": return "pack not loadable (no ModInfo.xml)"
    if "trader" in n: return "trader (would duplicate map traders)"
    if any(s in n for s in EXC) or "mpl_bridge" in t: return "needs water / bridge tile"
    return None
cand=[]; skipped={}
for r in inv:
    s=skip(r)
    if s: skipped.setdefault(s,[]).append(r["name"]); continue
    if not r.get("PrefabSize"): skipped.setdefault("no PrefabSize",[]).append(r["name"]); continue
    w,_,d=[int(v) for v in r["PrefabSize"].split(",")]
    cand.append((r,w,d))
cand.sort(key=lambda t:-(t[1]*t[2]))

taken=np.zeros((NB,NB),bool); placed=np.zeros((N,N),bool); out=[]; fails=[]; tally={}
rng=np.random.default_rng(20260904)
for r,w,d in cand:
    ab=(r.get("AllowedBiomes") or "").strip()
    allowed=[x.strip() for x in ab.split(",") if x.strip()] if ab else None
    got=None
    for ti,(flat,rd,spc) in enumerate(TIERS):
        pb=int(math.ceil(spc/B))
        for rot in (0,1,2,3):
            ww,dd=(d,w) if rot%2 else (w,d)
            free_,relief,hn,(fd,fw)=geo(ww,dd)
            f=free_&(relief<=flat)&(hn>=20.0)
            if rd is not None: f&=NEAR[rd]
            if allowed:
                am=np.zeros((NB,NB),bool)
                for a in allowed:
                    if a in NAMES: am|=(bname==NAMES.index(a))
                f&=am
            if not f.any(): continue
            # spacing: the *whole* footprint (+spacing) must be untaken, not just the corner
            tk=fwd(taken.astype(np.uint8), fd+2*pb, fw+2*pb, ndimage.maximum_filter, 0, back=pb)
            f&=(tk==0)
            idx=np.flatnonzero(f)
            if not idx.size: continue
            # exact, full-resolution re-check of every candidate corner (block grid rounds short)
            rng.shuffle(idx)
            for pick in idx[:400]:
                bz,bx=divmod(int(pick),NB); pz,px=bz*B,bx*B
                if occ[max(0,pz-BUF):pz+dd+BUF, max(0,px-BUF):px+ww+BUF].any(): continue
                if placed[max(0,pz-BUF):pz+dd+BUF, max(0,px-BUF):px+ww+BUF].any(): continue
                got=(rot,ww,dd,int(pick),ti,pb,fd,fw); break
            if got: break
        if got: break
    if not got: fails.append(r["name"]); continue
    rot,ww,dd,pick,ti,pb,fd,fw=got
    bz,bx=divmod(pick,NB)
    x=bx*B-HALF; z=bz*B-HALF
    sub=h[bz*B:bz*B+dd, bx*B:bx*B+ww]
    y=int(round(float(np.median(sub))))+1
    out.append({"name":r["name"],"mod":r["mod"],"x":x,"y":y,"z":z,"rot":rot,"w":ww,"d":dd,
                "tier":ti,"relief":round(float(sub.max()-sub.min()),2)})
    tally[ti]=tally.get(ti,0)+1
    taken[bz:bz+fd, bx:bx+fw]=True
    placed[bz*B:bz*B+dd, bx*B:bx*B+ww]=True

print("placed:",len(out),"failed:",len(fails))
for i,(fl,rd,s) in enumerate(TIERS):
    if tally.get(i): print(f"   tier{i}: relief<={fl}m road<={rd}m spacing {s}m -> {tally[i]}")
if fails: print("no site:",fails)
json.dump(out,open(os.path.join(SP,"placements.json"),"w"),indent=1)
json.dump(skipped,open(os.path.join(SP,"skipped.json"),"w"),indent=1)
