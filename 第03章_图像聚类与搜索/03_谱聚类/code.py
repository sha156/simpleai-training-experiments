# -*- coding: utf-8 -*-
# 实验3-3 谱聚类 —— 服务器端真实执行代码 (数据: 真实图像; 见 execution.log)
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


# ---------- exp03 谱聚类(人脸) ----------
def exp03():
    from sklearn.cluster import SpectralClustering, KMeans
    from sklearn.datasets import make_moons
    from sklearn.metrics import adjusted_rand_score
    from sklearn.metrics.pairwise import rbf_kernel
    log('\n'+'='*60); log('  实验3-3  谱聚类 Spectral Clustering'); log('='*60)
    faces=[('abma1','奥巴马'),('abma2','奥巴马'),('abma3','奥巴马'),('abma4','奥巴马'),
           ('bush1','布什'),('bush2','布什'),('jobs1','乔布斯'),('jobs2','乔布斯'),
           ('putin','普京'),('hawei','运动员')]
    X,thumbs,names=[],[],[]
    for fn,cn in faces:
        im=load_rgb(os.path.join(FACE,fn+'.jpg'))
        if im is None: log('  跳过缺失',fn); continue
        g=cv2.resize(cv2.cvtColor(im,cv2.COLOR_RGB2GRAY),(32,32)).astype(np.float32)
        g=(g-g.mean())/(g.std()+1e-6)
        X.append(np.concatenate([color_hist(im)*2,g.flatten()*0.3])); thumbs.append(thumb(im,72)); names.append(cn)
    X=np.array(X); log('真实人脸: %d 张 (%s)'%(len(X),', '.join(sorted(set(names)))))
    ncl=5
    lab=SpectralClustering(n_clusters=ncl,affinity='nearest_neighbors',n_neighbors=4,
                           random_state=42,assign_labels='discretize').fit_predict(X)
    log('谱聚类分组:')
    for cid in range(ncl):
        mem=[names[i] for i in range(len(lab)) if lab[i]==cid]
        if mem: log('  簇%d: %s'%(cid,' / '.join(mem)))
    RESULTS['exp03']={'n_faces':len(X),'n_clusters':ncl}
    order=np.argsort(lab)
    fig,axes=plt.subplots(1,len(order),figsize=(1.5*len(order),2.2))
    for ax,idx in zip(axes,order):
        ax.imshow(thumbs[idx]); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title('%s\n[%s%d]'%(names[idx],T('簇','C'),lab[idx]),fontproperties=FP,fontsize=9)
        for sp in ax.spines.values(): sp.set_color(plt.cm.tab10(lab[idx]/10.0)); sp.set_linewidth(3)
    fig.suptitle(T('谱聚类：真实人脸按相似度分组','Spectral clustering of faces'),fontproperties=FP,fontsize=13)
    save(fig,'exp03_faces_grouped.png')
    A=rbf_kernel(X,gamma=0.5)
    fig,ax=plt.subplots(figsize=(7,6)); im=ax.imshow(A,cmap='viridis')
    ax.set_xticks(range(len(names))); ax.set_yticks(range(len(names)))
    ax.set_xticklabels(names,rotation=90,fontproperties=FP,fontsize=8); ax.set_yticklabels(names,fontproperties=FP,fontsize=8)
    ax.set_title(T('人脸相似度矩阵 (RBF核)','Affinity matrix'),fontproperties=FP,fontsize=13)
    fig.colorbar(im,ax=ax,fraction=0.046); save(fig,'exp03_affinity.png')
    Xm,ym=make_moons(n_samples=300,noise=0.07,random_state=42)
    km=KMeans(n_clusters=2,n_init=10,random_state=42).fit_predict(Xm)
    scm=SpectralClustering(n_clusters=2,affinity='nearest_neighbors',random_state=42).fit_predict(Xm)
    fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    axes[0].scatter(Xm[:,0],Xm[:,1],c=km,cmap='coolwarm',s=12); axes[0].set_title('K-means (ARI=%.2f)'%adjusted_rand_score(ym,km),fontproperties=FP)
    axes[1].scatter(Xm[:,0],Xm[:,1],c=scm,cmap='coolwarm',s=12); axes[1].set_title(T('谱聚类','Spectral')+' (ARI=%.2f)'%adjusted_rand_score(ym,scm),fontproperties=FP)
    fig.suptitle(T('非凸数据：谱聚类优于K-means','Non-convex data'),fontproperties=FP,fontsize=13); save(fig,'exp03_moons_compare.png')


if __name__ == '__main__':
    build_vocab()
    exp03()
    print('结果:', RESULTS.get('exp03'))
