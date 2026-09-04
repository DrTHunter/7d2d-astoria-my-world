"""Place the 13 builds in a tight cluster near the player; flatness comes later from pads."""
import os,re,json,math,numpy as np
from PIL import Image
from scipy import ndimage
Image.MAX_IMAGE_PIXELS=None
SP=os.path.dirname(os.path.abspath(__file__))
OLD=os.path.join(os.path.dirname(os.path.abspath(__file__)), "work")
W=os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
LP=os.path.expandvars(r"%APPDATA%\7DaysToDie\LocalPrefabs")
N=8192;HALF=4096;B=4;NB=N//B;PX,PZ=2006,-989
APRON=6; RAMP=24; CLEAR=APRON+RAMP+4      # keep earthworks off existing POIs
h=np.load(os.path.join(OLD,"h.npy")); occ=np.load(os.path.join(SP,"occ_now.npy"))
sp3=np.array(Image.open(os.path.join(W,"splat3.png")))
road=(sp3[...,0]>100)|(sp3[...,1]>100); del sp3
occb=occ.reshape(NB,B,NB,B).any(axis=(1,3))
roadb=road.reshape(NB,B,NB,B).any(axis=(1,3))
hb=h.reshape(NB,B,NB,B);hmax=hb.max(axis=(1,3));hmin=hb.min(axis=(1,3));del hb
mg=48//B; occb[:mg,:]=occb[-mg:,:]=occb[:,:mg]=occb[:,-mg:]=True
rnear=ndimage.binary_dilation(roadb,ndimage.generate_binary_structure(2,2),iterations=45)
gy,gx=np.mgrid[0:NB,0:NB];wx=gx*B-HALF;wz=gy*B-HALF
sizes={}
for f in sorted(os.listdir(LP)):
    if not f.endswith(".xml"):continue
    b=f[:-4]
    if b=="Spotlight-down" or not os.path.exists(os.path.join(LP,b+".tts")):continue
    t=open(os.path.join(LP,f),encoding="utf-8",errors="replace").read()
    m=re.search(r'name="PrefabSize"\s+value="\s*(\d+),\s*(\d+),\s*(\d+)"',t)
    sizes[b]=(int(m.group(1)),int(m.group(3)))
mine=sorted(({"name":k,"w":v[0],"d":v[1]} for k,v in sizes.items()),key=lambda m:-(m["w"]*m["d"]))
print("prefabs:",len(mine),"total footprint %d m2"%sum(m["w"]*m["d"] for m in mine))
def freemask(w,d,cut):
    ob=int(math.ceil((w+2*CLEAR)/B));od=int(math.ceil((d+2*CLEAR)/B));bb=CLEAR//B
    o=ndimage.maximum_filter(occb.astype(np.uint8),size=(od,ob),mode='constant',cval=1,
                             origin=(-((od-1)//2)+bb,-((ob-1)//2)+bb))
    fw=int(math.ceil(w/B));fd=int(math.ceil(d/B))
    hx=ndimage.maximum_filter(hmax,size=(fd,fw),mode='constant',cval=1e4,origin=(-((fd-1)//2),-((fw-1)//2)))
    hn=ndimage.minimum_filter(hmin,size=(fd,fw),mode='constant',cval=-1e4,origin=(-((fd-1)//2),-((fw-1)//2)))
    return (o==0)&(hn>=24.0)&((hx-hn)<=cut), hx-hn
placed=[];newocc=np.zeros((N,N),bool)
pr=[m for m in mine if m["name"]=="Prison-perimiter"][0]
seed=None
for cut,rad in [(6,900),(9,900),(12,1200),(16,1600),(22,2200)]:
    ok,rel=freemask(pr["w"],pr["d"],cut)
    d0=np.hypot(wx+pr["w"]/2-PX,wz+pr["d"]/2-PZ)
    f=ok&(d0<=rad)&rnear
    idx=np.flatnonzero(f)
    if not idx.size:continue
    pick=int(idx[np.argmin(d0.ravel()[idx]+40*rel.ravel()[idx])])
    bz,bx=divmod(pick,NB)
    seed=(bx*B-HALF,bz*B-HALF,cut,float(d0.ravel()[pick]),float(rel.ravel()[pick]));break
assert seed,"no prison site"
SX,SZ,cut,dd,rl=seed
def commit(nm,x,z,w,d,rot):
    sub=h[z+HALF:z+HALF+d,x+HALF:x+HALF+w]
    placed.append({"name":nm,"x":x,"z":z,"w":w,"d":d,"rot":rot,
                   "H":int(round(float(np.median(sub)))),
                   "cut":round(float(sub.max()-np.median(sub)),1),
                   "fill":round(float(np.median(sub)-sub.min()),1)})
    newocc[z+HALF-APRON:z+HALF+d+APRON, x+HALF-APRON:x+HALF+w+APRON]=True
commit("Prison-perimiter",SX,SZ,pr["w"],pr["d"],0)
CX,CZ=SX+pr["w"]//2,SZ+pr["d"]//2
print(f"\nprison seed X={SX} Z={SZ}  {dd:.0f} m from you, native relief {rl:.1f} m (tier cut<={cut})")
fails=[]
for mm in mine:
    if mm["name"]=="Prison-perimiter":continue
    got=None
    for cut,rad in [(6,400),(9,550),(12,750),(16,1000),(24,1400),(32,2000)]:
        for rot in (0,1):
            w,d=(mm["d"],mm["w"]) if rot%2 else (mm["w"],mm["d"])
            ok,rel=freemask(w,d,cut)
            dc=np.hypot(wx+w/2-CX,wz+d/2-CZ)
            f=ok&(dc<=rad)
            idx=np.flatnonzero(f)
            if not idx.size:continue
            for pick in idx[np.argsort(dc.ravel()[idx]+25*rel.ravel()[idx])][:8000]:
                bz,bx=divmod(int(pick),NB);x,z=bx*B-HALF,bz*B-HALF
                X,Z=x+HALF,z+HALF
                if occ[Z-CLEAR:Z+d+CLEAR, X-CLEAR:X+w+CLEAR].any():continue
                if newocc[Z-APRON:Z+d+APRON, X-APRON:X+w+APRON].any():continue
                got=(x,z,w,d,rot);break
            if got:break
        if got:break
    if not got: fails.append(mm["name"]);continue
    commit(mm["name"],*got)
print(f"placed {len(placed)}/13   failed {fails}\n")
for p in sorted(placed,key=lambda q:math.hypot(q["x"]-CX,q["z"]-CZ)):
    print(f"   {p['name']:24} X={p['x']:6} Z={p['z']:6} {p['w']:3}x{p['d']:<3} rot {p['rot']}  "
          f"level {p['H']:3} m (cut {p['cut']:4.1f} / fill {p['fill']:4.1f})  "
          f"{math.hypot(p['x']-CX,p['z']-CZ):4.0f} m from prison")
xs=[p['x'] for p in placed]+[p['x']+p['w'] for p in placed]
zs=[p['z'] for p in placed]+[p['z']+p['d'] for p in placed]
print(f"\ncluster spans X {min(xs)}..{max(xs)}  Z {min(zs)}..{max(zs)}   "
      f"({max(xs)-min(xs)} x {max(zs)-min(zs)} m), {math.hypot(CX-PX,CZ-PZ):.0f} m from you")
json.dump({"placed":placed,"cx":CX,"cz":CZ,"apron":APRON,"ramp":RAMP},open(os.path.join(SP,"cluster.json"),"w"),indent=1)
