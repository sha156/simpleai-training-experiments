# -*- coding: utf-8 -*-
# 实验3-4 搜索结果排序 —— 服务器端真实执行代码 (数据: 真实图像; 见 execution.log)
# 环境: OpenCV3.4.2(SIFT) / sklearn0.23.2 / matplotlib3.3.3

import os, sys, json, time, glob, warnings, traceback
warnings.filterwarnings('ignore')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import cv2

ZH=True; FP=None
try:
    from matplotlib import font_manager as fm
    fm.fontManager.addfont('/tmp/simhei.ttf')
    FP=fm.FontProperties(fname='/tmp/simhei.ttf')
    plt.rcParams['font.family']=FP.get_name(); plt.rcParams['axes.unicode_minus']=False
except Exception as e:
    ZH=False; print('WARN font',e)
def T(zh,en): return zh if ZH else en

CV='/simpleware_ro/.notebook/data/ComputerVision'
FACE=CV+'/HierarCluster'; CAT=CV+'/101_ObjectCategories'
OUT='/tmp/out'; os.makedirs(OUT, exist_ok=True)
CATS=['accordion','airplanes','camera','elephant','butterfly','dolphin','sunflower','watch']
CN={'accordion':'手风琴','airplanes':'飞机','camera':'相机','elephant':'大象',
    'butterfly':'蝴蝶','dolphin':'海豚','sunflower':'向日葵','watch':'手表'}
RESULTS={}
def log(*a): print(*a); sys.stdout.flush()

def load_rgb(p,size=None):
    im=cv2.imread(p)
    if im is None: return None
    im=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
    return cv2.resize(im,size) if size else im
def cat_files(c,n,start=1): return sorted(glob.glob(os.path.join(CAT,c,'image_*.jpg')))[start-1:start-1+n]
def color_hist(im):
    hsv=cv2.cvtColor(im,cv2.COLOR_RGB2HSV)
    h=cv2.calcHist([hsv],[0,1],None,[12,8],[0,180,0,256]); cv2.normalize(h,h); return h.flatten()
def thumb(im,s=64): return cv2.resize(im,(s,s))
def save(fig,name):
    fig.savefig(os.path.join(OUT,name),dpi=110,bbox_inches='tight'); plt.close(fig); log('  saved',name)

# ---------- 共享 SIFT 视觉词汇 ----------
SIFT=cv2.xfeatures2d.SIFT_create(nfeatures=300)
VOC=200; _voc=None
def build_vocab():
    global _voc
    from sklearn.cluster import KMeans
    log('\n[预处理] 构建共享 SIFT 视觉词汇表 (K=%d)...'%VOC)
    desc=[]
    for c in CATS:
        for f in cat_files(c,10):
            g=cv2.imread(f,cv2.IMREAD_GRAYSCALE)
            if g is None: continue
            _,d=SIFT.detectAndCompute(g,None)
            if d is not None: desc.append(d)
    D=np.vstack(desc).astype(np.float32)
    log('  SIFT描述子总数 %d, 训练词汇表...'%len(D))
    _voc=KMeans(n_clusters=VOC,random_state=42,n_init=3).fit(D[:15000])
    log('  视觉词汇表就绪')
def bovw(path):
    g=cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    if g is None: return None
    _,d=SIFT.detectAndCompute(g,None)
    if d is None: return np.zeros(VOC)
    w=_voc.predict(d.astype(np.float32))
    h,_=np.histogram(w,bins=range(VOC+1))
    h=h.astype(np.float32)
    return h/(h.sum()+1e-6)
def feat_sem(path):
    im=load_rgb(path)
    return np.concatenate([bovw(path)*4.0, color_hist(im)*1.0])


# ---------- exp04 以图搜图(BoVW语义检索) ----------
def exp04():
    from sklearn.metrics.pairwise import cosine_similarity
    log('\n'+'='*60); log('  实验3-4  搜索结果排序 (SIFT-BoVW 语义检索)'); log('='*60)
    imgs,feats,cats=[],[],[]
    for c in CATS:
        for f in cat_files(c,8):
            b=bovw(f)
            if b is None: continue
            imgs.append(thumb(load_rgb(f),72)); feats.append(b); cats.append(c)
    DB=np.array(feats); log('图像数据库: %d 张 (%d类), 特征=SIFT-BoVW %d维'%(len(DB),len(CATS),VOC))
    qi=cats.index('accordion')
    sims=cosine_similarity([DB[qi]],DB).flatten()
    order=[o for o in np.argsort(sims)[::-1] if o!=qi][:8]
    log('查询图: %s'%CN['accordion']); log('  排名 相似度 类别')
    for r,o in enumerate(order): log('  #%d %.4f %s%s'%(r+1,sims[o],CN[cats[o]],'  ✓' if cats[o]=='accordion' else ''))
    rel=[1 if cats[o]=='accordion' else 0 for o in order]
    patk=[sum(rel[:i+1])/(i+1) for i in range(len(rel))]
    RESULTS['exp04']={'db':len(DB),'query':'accordion','P@8':patk[-1]}
    log('P@8=%.2f'%patk[-1])
    fig,axes=plt.subplots(1,9,figsize=(16,2.4))
    axes[0].imshow(imgs[qi]); axes[0].set_xticks([]); axes[0].set_yticks([])
    axes[0].set_title(T('查询\n%s'%CN['accordion'],'Query'),fontproperties=FP,fontsize=10)
    for sp in axes[0].spines.values(): sp.set_color('black'); sp.set_linewidth(2)
    for j,o in enumerate(order):
        ax=axes[j+1]; ax.imshow(imgs[o]); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title('#%d\n%.3f'%(j+1,sims[o]),fontproperties=FP,fontsize=9)
        col='#2ca02c' if cats[o]=='accordion' else '#d62728'
        for sp in ax.spines.values(): sp.set_color(col); sp.set_linewidth(3)
    fig.suptitle(T('以图搜图：查询「手风琴」的BoVW排序结果（绿框=正确）','BoVW retrieval'),fontproperties=FP,fontsize=13)
    save(fig,'exp04_retrieval.png')
    fig,ax=plt.subplots(figsize=(7,4.5)); ax.plot(range(1,len(patk)+1),patk,'o-',color='#2ca02c')
    ax.set_xlabel('k',fontproperties=FP); ax.set_ylabel('P@k',fontproperties=FP); ax.set_ylim(0,1.05); ax.grid(alpha=0.3)
    ax.set_title(T('检索准确率 P@k 曲线','Precision@k'),fontproperties=FP,fontsize=13); save(fig,'exp04_precision.png')


if __name__ == '__main__':
    build_vocab()
    exp04()
    print('结果:', RESULTS.get('exp04'))
