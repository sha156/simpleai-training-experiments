# -*- coding: utf-8 -*-
# 实验3-6 模式识别应用 —— 服务器端真实执行代码 (数据: 真实图像; 见 execution.log)
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


# ---------- exp06 BoVW+SVM 分类 ----------
def exp06():
    from sklearn.svm import LinearSVC
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import confusion_matrix, accuracy_score
    log('\n'+'='*60); log('  实验3-6  模式识别应用 (BoVW + SVM 分类)'); log('='*60)
    use=['accordion','airplanes','elephant','sunflower','watch']
    X,y,thumbs=[],[],[]
    for ci,c in enumerate(use):
        for f in cat_files(c,12):
            b=bovw(f)
            if b is None: continue
            X.append(b); y.append(ci); thumbs.append(thumb(load_rgb(f),64))
    X=np.array(X); y=np.array(y)
    Xtr,Xte,ytr,yte,ttr,tte=train_test_split(X,y,range(len(y)),test_size=0.35,random_state=42,stratify=y)
    clf=LinearSVC(C=1.0,max_iter=5000).fit(Xtr,ytr); pred=clf.predict(Xte); acc=accuracy_score(yte,pred)
    log('类别: %s'%', '.join(CN[c] for c in use)); log('训练/测试 %d/%d, 准确率 %.1f%%'%(len(ytr),len(yte),acc*100))
    RESULTS['exp06']={'classes':use,'accuracy':float(acc),'n':len(y)}
    cm=confusion_matrix(yte,pred)
    fig,ax=plt.subplots(figsize=(6.5,5.5)); im=ax.imshow(cm,cmap='Blues')
    ax.set_xticks(range(len(use))); ax.set_yticks(range(len(use)))
    ax.set_xticklabels([CN[c] for c in use],rotation=45,fontproperties=FP); ax.set_yticklabels([CN[c] for c in use],fontproperties=FP)
    for i in range(len(use)):
        for j in range(len(use)):
            ax.text(j,i,cm[i,j],ha='center',va='center',color='white' if cm[i,j]>cm.max()/2 else 'black',fontproperties=FP)
    ax.set_xlabel(T('预测','Pred'),fontproperties=FP); ax.set_ylabel(T('真实','True'),fontproperties=FP)
    ax.set_title(T('BoVW+SVM 混淆矩阵 (准确率 %.0f%%)'%(acc*100),'Confusion matrix'),fontproperties=FP,fontsize=13)
    save(fig,'exp06_confusion.png')
    fig,axes=plt.subplots(2,6,figsize=(14,5))
    for ax,k in zip(axes.ravel(),range(min(12,len(yte)))):
        ti=tte[k]; ax.imshow(thumbs[ti]); ax.set_xticks([]); ax.set_yticks([]); ok=pred[k]==yte[k]
        ax.set_title('%s\n→%s'%(CN[use[yte[k]]],CN[use[pred[k]]]),fontproperties=FP,fontsize=9,color='#2ca02c' if ok else '#d62728')
        for sp in ax.spines.values(): sp.set_color('#2ca02c' if ok else '#d62728'); sp.set_linewidth(3)
    fig.suptitle(T('测试样本分类结果（真实→预测）','Test predictions'),fontproperties=FP,fontsize=13)
    save(fig,'exp06_predictions.png')


if __name__ == '__main__':
    build_vocab()
    exp06()
    print('结果:', RESULTS.get('exp06'))
