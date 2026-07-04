# -*- coding: utf-8 -*-
# 实验3-5 创建视觉单词词汇 —— 服务器端真实执行代码 (数据: 真实图像; 见 execution.log)
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


# ---------- exp05 视觉词汇(手风琴 SIFT) ----------
def exp05():
    log('\n'+'='*60); log('  实验3-5  创建视觉单词词汇 Bag-of-Visual-Words'); log('='*60)
    acc=cat_files('accordion',6); kp_imgs=[]
    log('对手风琴 (accordion) 图像提取 SIFT 特征:')
    for f in acc:
        g=cv2.imread(f,cv2.IMREAD_GRAYSCALE); rgb=load_rgb(f)
        kp,_=SIFT.detectAndCompute(g,None)
        vis=cv2.drawKeypoints(rgb,kp,None,color=(255,0,0),flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        kp_imgs.append((thumb(vis,120),len(kp))); log('  %s : %d 个关键点'%(os.path.basename(f),len(kp)))
    RESULTS['exp05']={'vocab':VOC,'accordion_imgs':len(acc)}
    fig,axes=plt.subplots(2,3,figsize=(12,8))
    for ax,(vis,nk) in zip(axes.ravel(),kp_imgs):
        ax.imshow(vis); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(T('SIFT关键点: %d'%nk,'%d kp'%nk),fontproperties=FP,fontsize=11)
    fig.suptitle(T('手风琴 (accordion) 图像的 SIFT 特征点','SIFT keypoints on accordion'),fontproperties=FP,fontsize=15)
    save(fig,'exp05_sift_keypoints.png')
    # 词汇量 vs inertia
    from sklearn.cluster import KMeans
    desc=[]
    for c in CATS:
        for f in cat_files(c,6):
            g=cv2.imread(f,cv2.IMREAD_GRAYSCALE)
            if g is None: continue
            _,d=SIFT.detectAndCompute(g,None)
            if d is not None: desc.append(d)
    Dd=np.vstack(desc).astype(np.float32); log('描述子总数 %d 个(128维)'%len(Dd))
    sizes=[50,100,200,400]; inertias=[]
    for vs in sizes:
        inertias.append(KMeans(n_clusters=vs,random_state=42,n_init=3).fit(Dd[:8000]).inertia_)
        log('  词汇量=%d inertia=%.0f'%(vs,inertias[-1]))
    fig,ax=plt.subplots(figsize=(7,4.5)); ax.plot(sizes,inertias,'o-',color='#9467bd')
    ax.set_xlabel(T('视觉词汇量','Vocab size'),fontproperties=FP); ax.set_ylabel('Inertia',fontproperties=FP)
    ax.set_title(T('视觉词汇表规模对紧致度的影响','Vocab size vs inertia'),fontproperties=FP,fontsize=13); ax.grid(alpha=0.3)
    save(fig,'exp05_vocab_size.png')
    # BoW直方图
    b=bovw(acc[0]);
    fig,axes=plt.subplots(1,2,figsize=(13,4.2),gridspec_kw={'width_ratios':[1,2.4]})
    axes[0].imshow(load_rgb(acc[0])); axes[0].axis('off'); axes[0].set_title(T('输入：手风琴','Input'),fontproperties=FP,fontsize=12)
    axes[1].bar(range(VOC),b,color='#9467bd',width=1.0)
    axes[1].set_xlabel(T('视觉单词编号','Word id'),fontproperties=FP); axes[1].set_ylabel(T('归一化频率','freq'),fontproperties=FP)
    axes[1].set_title(T('该图的视觉单词直方图 (BoVW编码)','BoVW histogram'),fontproperties=FP,fontsize=12)
    save(fig,'exp05_bow_histogram.png')


if __name__ == '__main__':
    build_vocab()
    exp05()
    print('结果:', RESULTS.get('exp05'))
