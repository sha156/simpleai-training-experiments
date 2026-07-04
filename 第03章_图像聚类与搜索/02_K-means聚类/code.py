# -*- coding: utf-8 -*-
# 实验3-2 K-means聚类 —— 服务器端真实执行代码 (数据: 真实图像; 见 execution.log)
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


# ---------- exp02 K-means ----------
def exp02():
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    from sklearn.decomposition import PCA
    log('\n'+'='*60); log('  实验3-2  K-means 聚类'); log('='*60)
    use=['accordion','airplanes','elephant','sunflower','watch','dolphin']
    X,thumbs=[],[]
    for c in use:
        for f in cat_files(c,5):
            ft=feat_sem(f)
            if ft is None: continue
            X.append(ft); thumbs.append(thumb(load_rgb(f),56))
    X=np.array(X); log('样本: %d 张真实图像, 特征=SIFT-BoVW+颜色 %d维'%(len(X),X.shape[1]))
    ks=list(range(2,9)); inertia=[]; sil=[]
    for kk in ks:
        km=KMeans(n_clusters=kk,random_state=42,n_init=10).fit(X)
        inertia.append(km.inertia_); sil.append(silhouette_score(X,km.labels_))
        log('  k=%d inertia=%.3f 轮廓=%.4f'%(kk,km.inertia_,sil[-1]))
    bestk=ks[int(np.argmax(sil))]
    RESULTS['exp02']={'n':len(X),'best_k':int(bestk),'best_sil':float(max(sil))}
    log('最佳 k=%d (轮廓系数 %.4f)'%(bestk,max(sil)))
    fig,ax1=plt.subplots(figsize=(8,5))
    ax1.plot(ks,inertia,'o-',color='#1f77b4'); ax1.set_xlabel('K',fontproperties=FP)
    ax1.set_ylabel(T('簇内平方和','Inertia'),color='#1f77b4',fontproperties=FP)
    ax2=ax1.twinx(); ax2.plot(ks,sil,'s-',color='#d62728')
    ax2.set_ylabel(T('轮廓系数','Silhouette'),color='#d62728',fontproperties=FP)
    ax1.axvline(bestk,ls='--',color='gray')
    ax1.set_title(T('肘部法则 + 轮廓系数选择 K','Elbow + Silhouette'),fontproperties=FP,fontsize=14)
    save(fig,'exp02_elbow_silhouette.png')
    km=KMeans(n_clusters=bestk,random_state=42,n_init=10).fit(X); lab=km.labels_
    fig,axes=plt.subplots(bestk,6,figsize=(11,1.8*bestk))
    if bestk==1: axes=[axes]
    for cid in range(bestk):
        mem=np.where(lab==cid)[0][:6]
        for j in range(6):
            ax=axes[cid][j]; ax.axis('off')
            if j<len(mem): ax.imshow(thumbs[mem[j]])
        axes[cid][0].axis('on'); axes[cid][0].set_xticks([]); axes[cid][0].set_yticks([])
        axes[cid][0].set_ylabel(T('簇%d'%cid,'C%d'%cid),fontproperties=FP,rotation=0,labelpad=20)
    fig.suptitle(T('K-means 各簇的真实图像','K-means clusters'),fontproperties=FP,fontsize=14)
    save(fig,'exp02_clusters.png')
    P=PCA(n_components=2).fit_transform(X)
    fig,ax=plt.subplots(figsize=(9,7)); ax.scatter(P[:,0],P[:,1],c=lab,cmap='tab10',s=10)
    for i in range(0,len(P),2):
        ax.add_artist(AnnotationBbox(OffsetImage(thumbs[i],zoom=0.28),(P[i,0],P[i,1]),frameon=False))
    ax.set_title(T('K-means 聚类 (PCA 2D + 真实缩略图)','K-means PCA'),fontproperties=FP,fontsize=14)
    save(fig,'exp02_pca_scatter.png')


if __name__ == '__main__':
    build_vocab()
    exp02()
    print('结果:', RESULTS.get('exp02'))
