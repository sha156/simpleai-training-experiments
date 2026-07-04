# 实验配方：让结果"有意义 + 有真实实例图"

用户要的不是随便跑通，而是图里能看到**真实图片**、指标看着**合理**。下面是"图像聚类与搜索"这一章
（PCV 教材 6/7 章）验证过的配方，也是通用原则的示例。

## 通用原则

1. **图里直接画真实图**。终端日志有数字就够了？不够。每个实验至少一张图要包含真实缩略图：
   - 聚类 → 树状图叶节点放真实缩略图；每个簇画一行真实图 montage。
   - 检索 → "查询图 + top-N 检索结果"横排，同类绿框、异类红框，标相似度。
   - 特征 → 用 `cv2.drawKeypoints` 把 SIFT 关键点画在真实图上。
   - 分类 → 测试样本真实图，标"真实标签→预测标签"，对错用绿/红边框。
   - 用 matplotlib 的 `OffsetImage` + `AnnotationBbox` 往坐标/树状图上贴缩略图；贴在轴外用
     `xycoords='data', boxcoords='offset points'`（否则会把坐标轴撑出巨大空白）。

2. **特征要配得上任务**。低层颜色直方图区分 Caltech 物体很弱（背景杂、同类颜色差异大）。
   语义任务（聚类/检索/分类）用 **SIFT-BoVW**（先建一次视觉词汇，各图编码成词频直方图），
   效果和"是否出现真实同类图"都明显更好。本章实测：颜色特征检索手风琴 P@5≈0.2，换 BoVW 后 P@8≈0.62。

3. **方法用在它擅长的地方**。感知哈希（aHash/dHash/pHash）是给**近重复检测**用的，不是语义检索。
   直接拿它在 Caltech 里"检索同类"必然接近随机（各是不同实例）。正确演示：对一张查询图做
   JPEG 压缩/缩放/模糊/调亮/旋转等**失真变换**，证明哈希对这些变换汉明距离很小（鲁棒），
   再把这些变换版塞进图库让哈希"找回自己的失真版"——P@5 轻松到 1.0，既正确又好看。

4. **诚实**。指标低就低（如聚类轮廓系数~0.12 是 Caltech 低层特征的真实难度），在文档里说明，
   但保证图里真实展示了分组/检索过程。一张图读不进去（中文变方框、算法出错）就必须修，不能糊过去。

5. **每个实验存**：`若干 PNG` + `results.json`（关键指标）+ 中文 stdout（做终端截图用）。
   用 `try/except` 包住每个实验，互不牵连。

## 本章 7 个实验的配方（可直接照搬/改造）

| 实验 | 真实数据 | 方法 | 出的实例图 |
|------|---------|------|-----------|
| 层次聚类 | Caltech 6 类×4 张 | SIFT-BoVW+HSV颜色 → ward linkage | 树状图(叶=真实缩略图)、按簇分组 montage、连接方式对比 |
| K-means | 同上 6 类×5 张 | 同特征 → KMeans | 肘部+轮廓曲线、各簇真实图、PCA 散点贴缩略图 |
| 谱聚类 | 真实人脸 9~10 张 | 颜色+灰度 → 近邻谱聚类 | 人脸按相似度分组、相似度矩阵热图、两月形 K-means vs 谱聚类 |
| 搜索排序 | Caltech 8 类×8 张图库 | SIFT-BoVW 余弦相似度 | 查询"手风琴"→top8 检索结果(绿/红框)、P@k 曲线 |
| 视觉词汇 BoVW | 手风琴 6 张 + 8 类 | SIFT + KMeans(200词) | **手风琴 SIFT 关键点图**、词汇量 vs inertia、某图 BoVW 直方图 |
| 模式识别 | 5 类×12 张 | BoVW + LinearSVC | 混淆矩阵、测试样本"真实→预测"图 |
| 哈希检索 | 向日葵 1 张+6 变换+48 干扰 | aHash/dHash/pHash | 变换鲁棒性(各变换汉明距离)、近重复检索、三方法 P@5 对比 |

## 服务器端脚本骨架

```python
# -*- coding: utf-8 -*-
import os, json, glob, warnings, traceback
warnings.filterwarnings('ignore')
import numpy as np, cv2
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

fm.fontManager.addfont('/tmp/simhei.ttf')
FP = fm.FontProperties(fname='/tmp/simhei.ttf')
plt.rcParams['font.family'] = FP.get_name(); plt.rcParams['axes.unicode_minus'] = False

CV = '/simpleware_ro/.notebook/data/ComputerVision'
CAT = CV + '/101_ObjectCategories'
OUT = '/tmp/out'; os.makedirs(OUT, exist_ok=True)
SIFT = cv2.xfeatures2d.SIFT_create(nfeatures=300)   # 注意 xfeatures2d，OpenCV 3.4.2

def load_rgb(p, size=None):
    im = cv2.imread(p)
    if im is None: return None
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    return cv2.resize(im, size) if size else im

RESULTS = {}
def exp01():
    ...  # 对真实图跑算法，plt 存图到 OUT，往 RESULTS 写指标
    plt.savefig(os.path.join(OUT, 'exp01_xxx.png'), dpi=110, bbox_inches='tight')

for name, fn in [('exp01', exp01), ...]:
    try: fn()
    except Exception: print('ERROR', name); print(traceback.format_exc())

json.dump(RESULTS, open(OUT + '/results.json', 'w'), ensure_ascii=False, indent=2)
open(OUT + '/DONE', 'w').write('ok')     # 轮询用的完成标记
```

## 整理进文件夹 + 终端截图（本地）

参考本次会话在项目里生成的 `organize.py`：把主脚本按 `# ---------- expNN` 标记切成"共享前导 + 各实验函数"，
每个实验文件夹写 `code.py`（前导+该函数+`__main__`）；日志按"实验3-N"标题切段写 `execution.log`；
用 `scripts/terminal_screenshot.py`：

```python
from terminal_screenshot import create_terminal_screenshot, GREEN, YELLOW, CYAN, RED, FG
lines = [('$ python3 run_experiments_real.py    # 服务器真实执行', '#569CD6'), ('', FG)]
# 把真实 log 逐行上色：'='*60→GREEN, 含"实验3-N"→YELLOW, "saved …"→CYAN, 含✓/准确率/P@→GREEN
create_terminal_screenshot(lines, '实验3-5 …(SimpleAI 10.248.6.104)', 'terminal.png',
                           output_dir=fdir, font_size=14, width=980)
```

生成后**务必 Read 出来看**：中文是否正常、结果是否合理。中文变方框 = 字体没加载成功（检查 `/tmp/simhei.ttf`）。
