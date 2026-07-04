# -*- coding: utf-8 -*-
# 实验3-7 哈希图像检索比较 —— 服务器端真实执行代码 (数据: 真实图像; 见 execution.log)
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


# ---------- exp07 哈希近重复检索(变换鲁棒性) ----------
def exp07():
    log('\n'+'='*60); log('  实验3-7  哈希图像检索比较 (感知哈希·近重复检索)'); log('='*60)
    def ahash(g): s=cv2.resize(g,(8,8)); return (s>s.mean()).flatten()
    def dhash(g): s=cv2.resize(g,(9,8)); return (s[:,1:]>s[:,:-1]).flatten()
    def phash(g):
        s=cv2.resize(g,(32,32)).astype(np.float32); dct=cv2.dct(s)[:8,:8]; return (dct>np.median(dct)).flatten()
    methods={'aHash':ahash,'dHash':dhash,'pHash':phash}
    # 查询图 + 6种变换(模拟传播中的失真) -> 近重复
    qf=cat_files('sunflower',1)[0]; q_rgb=load_rgb(qf); q_gray=cv2.imread(qf,cv2.IMREAD_GRAYSCALE)
    h,w=q_gray.shape
    def jpeg(g,q):
        _,e=cv2.imencode('.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,q]); return cv2.imdecode(e,cv2.IMREAD_GRAYSCALE)
    trans=[('原图',q_gray),('JPEG压缩',jpeg(q_gray,20)),('缩放50%',cv2.resize(cv2.resize(q_gray,(w//2,h//2)),(w,h))),
           ('高斯模糊',cv2.GaussianBlur(q_gray,(7,7),0)),('调亮',np.clip(q_gray.astype(int)+45,0,255).astype(np.uint8)),
           ('旋转5°',cv2.warpAffine(q_gray,cv2.getRotationMatrix2D((w/2,h/2),5,1),(w,h)))]
    trans_rgb=[('原图',q_rgb),('JPEG压缩',None),('缩放50%',None),('高斯模糊',None),('调亮',None),('旋转5°',None)]
    log('查询图 %s + 6种失真变换(近重复):'%CN['sunflower'])
    # 图A: 变换鲁棒性 - 各变换相对原图的汉明距离
    ref={n:fn(q_gray) for n,fn in methods.items()}
    fig,axes=plt.subplots(1,6,figsize=(15,3))
    for ax,(nm,g) in zip(axes,trans):
        vis=cv2.cvtColor(g,cv2.COLOR_GRAY2RGB) if nm!='原图' else q_rgb
        ax.imshow(vis if nm=='原图' else cv2.cvtColor(g,cv2.COLOR_GRAY2RGB)); ax.set_xticks([]); ax.set_yticks([])
        ds=' '.join('%s=%d'%(m,int(np.sum(ref[m]!=fn(g)))) for m,fn in methods.items())
        ax.set_title(nm+'\n'+ds,fontproperties=FP,fontsize=9)
        log('  %s : %s'%(nm,ds))
    fig.suptitle(T('感知哈希对失真的鲁棒性（汉明距离越小越稳健）','Hash robustness to distortions'),fontproperties=FP,fontsize=13)
    save(fig,'exp07_robustness.png')
    # 近重复检索: 池 = 变换版本(近重复) + 干扰图, 用原图查询
    pool_g=[t[1] for t in trans[1:]]; pool_rgb=[cv2.cvtColor(t[1],cv2.COLOR_GRAY2RGB) for t in trans[1:]]; pool_isdup=[1]*5
    for c in CATS:
        for f in cat_files(c,6,start=3):
            g=cv2.imread(f,cv2.IMREAD_GRAYSCALE)
            if g is None: continue
            pool_g.append(g); pool_rgb.append(load_rgb(f)); pool_isdup.append(0)
    log('近重复检索池: %d 张 (5张近重复 + %d张干扰)'%(len(pool_g),len(pool_g)-5))
    prec={}; retr={}
    for name,fn in methods.items():
        qc=fn(q_gray); codes=[fn(g) for g in pool_g]
        dist=[int(np.sum(qc!=codes[i])) for i in range(len(codes))]
        order=list(np.argsort(dist))[:5]
        prec[name]=sum(pool_isdup[o] for o in order)/5.0; retr[name]=(order,dist)
        log('  %s : P@5=%.2f (前5命中近重复 %d/5)'%(name,prec[name],int(prec[name]*5)))
    RESULTS['exp07']={'pool':len(pool_g),'dups':5,'precision':{k:float(v) for k,v in prec.items()}}
    fig,axes=plt.subplots(3,6,figsize=(14,7.2))
    for r,name in enumerate(methods):
        order,dist=retr[name]
        axes[r][0].imshow(q_rgb); axes[r][0].set_xticks([]); axes[r][0].set_yticks([])
        axes[r][0].set_ylabel(name,fontproperties=FP,fontsize=13,rotation=0,labelpad=25)
        axes[r][0].set_title(T('查询','Query') if r==0 else '',fontproperties=FP,fontsize=10)
        for sp in axes[r][0].spines.values(): sp.set_color('black'); sp.set_linewidth(2)
        for j,o in enumerate(order):
            ax=axes[r][j+1]; ax.imshow(pool_rgb[o]); ax.set_xticks([]); ax.set_yticks([])
            ax.set_title('d=%d'%dist[o],fontproperties=FP,fontsize=9)
            col='#2ca02c' if pool_isdup[o] else '#d62728'
            for sp in ax.spines.values(): sp.set_color(col); sp.set_linewidth(3)
    fig.suptitle(T('哈希近重复检索：查询「向日葵」找回其失真版本（绿框=近重复）','Near-duplicate retrieval'),fontproperties=FP,fontsize=14)
    save(fig,'exp07_hash_retrieval.png')
    fig,axes=plt.subplots(1,2,figsize=(13,4.5))
    axes[0].bar(list(prec.keys()),list(prec.values()),color=['#1f77b4','#ff7f0e','#2ca02c']); axes[0].set_ylim(0,1.08)
    axes[0].set_ylabel('P@5',fontproperties=FP); axes[0].set_title(T('三种哈希近重复检索准确率','Precision'),fontproperties=FP,fontsize=12)
    for i,(k,v) in enumerate(prec.items()): axes[0].text(i,v+0.02,'%.2f'%v,ha='center',fontproperties=FP)
    code=phash(q_gray).reshape(8,8); axes[1].imshow(code,cmap='gray')
    axes[1].set_title(T('向日葵的 pHash 64位指纹','pHash fingerprint'),fontproperties=FP,fontsize=12); axes[1].set_xticks([]); axes[1].set_yticks([])
    save(fig,'exp07_hash_compare.png')


if __name__ == '__main__':
    build_vocab()
    exp07()
    print('结果:', RESULTS.get('exp07'))
