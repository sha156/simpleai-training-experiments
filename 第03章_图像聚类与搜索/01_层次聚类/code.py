# -*- coding: utf-8 -*-
# 实验3-1 层次聚类 —— 服务器端真实执行代码 (数据: 真实图像; 见 execution.log)
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


# ---------- exp01 层次聚类 ----------
def exp01():
    from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
    from sklearn.metrics import silhouette_score
    log('\n'+'='*60); log('  实验3-1  层次聚类 Hierarchical Clustering'); log('='*60)
    use=['accordion','airplanes','elephant','sunflower','watch','dolphin']
    X,labels,thumbs=[],[],[]
    for ci,c in enumerate(use):
        for f in cat_files(c,4):
            ft=feat_sem(f)
            if ft is None: continue
            X.append(ft); labels.append(ci); thumbs.append(thumb(load_rgb(f),56))
    X=np.array(X); labels=np.array(labels)
    log('样本: %d 张真实图像 (%d类: %s)'%(len(X),len(use),', '.join(CN[c] for c in use)))
    log('特征: SIFT-BoVW(%d) + HSV颜色直方图, 共%d维'%(VOC,X.shape[1]))
    Z=linkage(X,method='ward')
    for k in (4,5,6): log('  k=%d 轮廓系数=%.4f'%(k,silhouette_score(X,fcluster(Z,k,'maxclust'))))
    k=len(use); cl=fcluster(Z,k,'maxclust')
    RESULTS['exp01']={'n':len(X),'classes':use,'silhouette':float(silhouette_score(X,cl))}
    # 树状图 + 缩略图(offset points 修正间距)
    fig,ax=plt.subplots(figsize=(13,4.2))
    dd=dendrogram(Z,ax=ax,color_threshold=Z[-(k-1),2],leaf_rotation=90,no_labels=True)
    ax.set_title(T('层次聚类树状图（叶节点为真实图像）','Hierarchical Dendrogram'),fontproperties=FP,fontsize=15)
    ax.set_ylabel(T('簇间距离','distance'),fontproperties=FP); ax.set_xticks([])
    for i,idx in enumerate(dd['leaves']):
        x=5+i*10
        ab=AnnotationBbox(OffsetImage(thumbs[idx],zoom=0.42),(x,0),xybox=(0,-34),
              xycoords='data',boxcoords='offset points',frameon=True,box_alignment=(0.5,1),pad=0.1,
              bboxprops=dict(edgecolor=plt.cm.tab10(labels[idx]/10.0),lw=2))
        ax.add_artist(ab)
    save(fig,'exp01_dendrogram.png')
    # 分组蒙太奇
    per={}; [per.setdefault(cl[i],[]).append(i) for i in np.argsort(cl)]
    fig,axes=plt.subplots(k,4,figsize=(8,2*k))
    for r,(cid,items) in enumerate(sorted(per.items())):
        for cpos in range(4):
            ax=axes[r][cpos]; ax.axis('off')
            if cpos<len(items): ax.imshow(thumbs[items[cpos]])
            if cpos==0:
                ax.axis('on'); ax.set_xticks([]); ax.set_yticks([])
                ax.set_ylabel(T('簇%d'%cid,'C%d'%cid),fontproperties=FP,fontsize=12,rotation=0,labelpad=22)
    fig.suptitle(T('层次聚类结果：真实图像按簇分组','Clusters of real images'),fontproperties=FP,fontsize=14)
    save(fig,'exp01_clusters.png')
    # 连接方式对比
    fig,axes=plt.subplots(1,3,figsize=(15,4))
    for ax,m in zip(axes,['ward','complete','average']):
        Zi=linkage(X,method=m); dendrogram(Zi,ax=ax,no_labels=True,color_threshold=Zi[-(k-1),2])
        ax.set_title(T('%s 连接'%m,m),fontproperties=FP)
    fig.suptitle(T('层次聚类：连接方式对比','Linkage comparison'),fontproperties=FP,fontsize=14)
    save(fig,'exp01_linkage_compare.png')


if __name__ == '__main__':
    build_vocab()
    exp01()
    print('结果:', RESULTS.get('exp01'))
