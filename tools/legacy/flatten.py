"""Level a pad under each of the 13 builds, with a cosine ramp back to natural terrain."""
import os,json,shutil,numpy as np
from scipy import ndimage
SP=os.path.dirname(os.path.abspath(__file__))
W=os.path.expandvars(r"%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K")
DTM=os.path.join(W,"dtm.raw"); BAK=DTM+".ORIGINAL-BACKUP"
N=8192;HALF=4096
cfg=json.load(open(os.path.join(SP,"cluster.json")))
pl=cfg["placed"]; APRON=cfg["apron"]; RAMP=cfg["ramp"]
occ=np.load(os.path.join(SP,"occ_now.npy"))
if not os.path.exists(BAK): shutil.copy2(DTM,BAK); print("backed up dtm.raw")
raw=np.fromfile(BAK,dtype="<u2").reshape(N,N)
h=raw.astype(np.float32)/256.0
xs=[p["x"] for p in pl]+[p["x"]+p["w"] for p in pl]
zs=[p["z"] for p in pl]+[p["z"]+p["d"] for p in pl]
PAD=RAMP+16
x0=min(xs)+HALF-PAD; x1=max(xs)+HALF+PAD; z0=min(zs)+HALF-PAD; z1=max(zs)+HALF+PAD
win=h[z0:z1, x0:x1].copy(); H0=win.copy()
core=np.zeros(win.shape,bool); tgt=np.zeros(win.shape,np.float32)
for p in pl:
    a=p["z"]+HALF-z0-APRON; b=a+p["d"]+2*APRON
    c=p["x"]+HALF-x0-APRON; d=c+p["w"]+2*APRON
    core[a:b, c:d]=True; tgt[a:b, c:d]=p["H"]
dist,(iy,ix)=ndimage.distance_transform_edt(~core,return_indices=True)
near=tgt[iy,ix]
w=np.zeros(win.shape,np.float32)
band=(dist>0)&(dist<=RAMP)
w[band]=0.5*(1+np.cos(np.pi*dist[band]/RAMP))
new=np.where(core,tgt,H0*(1-w)+near*w)
touched=(np.abs(new-H0)>1e-4)
occw=occ[z0:z1, x0:x1]
clash=int((touched&occw).sum())
print("pixels whose height changes:",int(touched.sum()))
print("of those, under an existing POI:",clash)
assert clash==0, "earthworks would disturb an existing POI"
print("max cut %.1f m   max fill %.1f m"%(float((H0-new)[touched].max()),float((new-H0)[touched].max())))
h[z0:z1, x0:x1]=new
out=np.clip(np.round(h*256.0),0,65535).astype("<u2")
out.tofile(DTM)
print("wrote dtm.raw")
chk=np.fromfile(DTM,dtype="<u2").reshape(N,N).astype(np.float32)/256.0
bad=[]
for p in pl:
    s=chk[p["z"]+HALF:p["z"]+HALF+p["d"], p["x"]+HALF:p["x"]+HALF+p["w"]]
    r=float(s.max()-s.min())
    if r>0.02: bad.append((p["name"],round(r,3)))
    p["y"]=int(round(float(s.mean())))+1
print("footprints not perfectly level:",bad if bad else "none - all 13 are flat")
for f in ("dtm_processed.raw",):
    q=os.path.join(W,f)
    if os.path.exists(q): os.remove(q); print("removed",f,"(game regenerates it)")
json.dump(cfg,open(os.path.join(SP,"cluster.json"),"w"),indent=1)
