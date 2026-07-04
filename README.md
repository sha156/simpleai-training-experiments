# SimpleAI 智能系统开发及部署实训

> **SimpleAI Intelligent System Development & Deployment Training**
>
> 19 章节 · 103 实验 · TensorFlow / OpenCV / CNN & RNN / 区块链 / 网络爬虫

## 项目概述

本仓库为 **SimpleAI 人工智能教学实训系统** 上完成的「智能系统开发及部署实训」课程全部实验成果。

- **平台**：SimpleAI 人工智能教学实训系统
- **课程**：智能系统开发及部署实训
- **教师**：张罡
- **时间**：2026-06-27 ~ 2026-07-08
- **总章节**：19 · **总实验**：103

## 目录结构

```
├── README.md                          ← 本文件
├── skill/                             ← Claude Code Skill：真实实验流水线工具集
│   ├── README.md                      #   使用说明与注意事项
│   ├── SKILL.md                       #   Skill 定义（触发条件、标准流程）
│   ├── references/                    #   连接故障对策 + 实验设计配方
│   └── scripts/                       #   srv.py (SSH助手) + terminal_screenshot.py (截图工具)
├── crawled_data/                      ← 平台抓取数据（课程结构、成绩、实验详情等）
│   ├── 01_all_experiments.json        # 全部实验列表
│   ├── 01_course_structure.json       # 课程结构
│   ├── 02_all_requirements.md         # 全部实验要求汇总
│   ├── *.json / *.html                # 各页面抓取数据
│   └── ...
├── 第01章_TensorFlow环境搭建/          ← TensorFlow 安装与基础运算
├── 第02章_TensorFlow基础知识与可视化表示/ ← 数据流水线、TensorBoard
├── 第03章_图像聚类与搜索/              ← 层次/K-means/谱聚类、SIFT、BoVW、哈希检索 ✅
├── 第04章_CNN与RNN原理与实现/          ← CNN/NiN/RNN/BPTT 真实训练 ✅
├── 第05章_基本图像处理运算/            ← 图像读取、灰度化、直方图、几何变换
├── 第06章_图像滤波/                    ← 空间域/频率域滤波
├── 第07章_图像分割/                    ← 阈值分割、区域生长、分水岭
├── 第08章_OpenCV_OpenGL/              ← 绘图函数、鼠标交互、Trackbar
├── 第09章_特征提取/                    ← SIFT/HOG/LBP/颜色直方图/GLCM
├── 第10章_描述子与角点检测/            ← Harris/ShiTomasi/SIFT匹配/图像拼接
├── 第11章_CNN与RNN实例/               ← CNN分类/迁移学习/RNN文本分类/GRU/LSTM
├── 第12章_TensorFlow综合人脸识别/      ← TF 人脸识别实战
├── 第13章_三维视觉/                    ← 立体视觉、深度图、点云
├── 第14章_运动对象检测/               ← 帧差法/背景减除/光流/MeanShift
├── 第15章_网络爬虫/                    ← HTTP/Scrapy/异步/分布式/反爬虫
├── 第16章_概率图模型/                  ← 贝叶斯网络/HMM/CRF/MRF
├── 第17章_机器学习图像处理/            ← SVM/KNN/随机森林/KMeans/PCA
├── 第18章_语音识别/                    ← MFCC/语音识别/语音合成
└── 第19章_区块链/                      ← 哈希/工作量证明/加密货币/智能合约/NFT
```

## 章节进度

| 章节 | 名称 | 实验数 | 状态 |
|------|------|--------|------|
| 第01章 | TensorFlow环境搭建 | 1 | ✅ |
| 第02章 | TensorFlow基础知识与可视化表示 | 2 | ✅ |
| 第03章 | 图像聚类与搜索 | 7 | ✅ 含真实图像实例 |
| 第04章 | CNN与RNN原理与实现 | 4 | ✅ TF真实训练 |
| 第05章 | 基本图像处理运算 | 9 | ✅ |
| 第06章 | 图像滤波 | 2 | ✅ |
| 第07章 | 图像分割 | 2 | ✅ |
| 第08章 | OpenCV/OpenGL | 5 | ✅ |
| 第09章 | 特征提取 | 7 | ✅ |
| 第10章 | 描述子与角点检测 | 4 | ✅ |
| 第11章 | CNN与RNN实例 | 7 | ✅ |
| 第12章 | TensorFlow综合人脸识别 | 1 | ✅ |
| 第13章 | 三维视觉 | 2 | ✅ |
| 第14章 | 运动对象检测 | 5 | ✅ |
| 第15章 | 网络爬虫 | 13 | ✅ |
| 第16章 | 概率图模型 | 4 | ✅ |
| 第17章 | 机器学习图像处理 | 6 | ✅ |
| 第18章 | 语音识别 | 5 | ✅ |
| 第19章 | 区块链 | 17 | ✅ |

## 重点章节结果展示

### 第03章 — 图像聚类与搜索

使用 **真实图像**（人脸、Caltech-101）在实验服务器上执行，包含 SIFT 特征提取与 BoVW 模型。

| 实验 | 内容 | 关键结果 |
|------|------|----------|
| 01 层次聚类 | 6类×4张真实图，SIFT-BoVW+颜色特征 | 树状图叶节点=真实缩略图, 轮廓系数 0.12 |
| 02 K-means聚类 | 6类×5张真实图 | 肘部+轮廓选 k=3, 各簇真实图 montage |
| 03 谱聚类 | 9张真实人脸 | 乔布斯对正确聚合 |
| 04 搜索结果排序 | 64张(8类)图库, SIFT-BoVW余弦 | 手风琴 top5 全对, P@8=0.625 |
| 05 创建视觉词汇 | 手风琴+8类, SIFT+K-means(200词) | SIFT 关键点可视化 |
| 06 模式识别 | 5类×12张, BoVW+LinearSVC | 混淆矩阵, 准确率 57% |
| 07 哈希检索比较 | 向日葵+6变换+48干扰, aHash/dHash/pHash | 近重复检索 P@5=1.0 |

### 第04章 — CNN与RNN原理与实现

TensorFlow 2.21 真实训练，含训练曲线、混淆矩阵、特征图等。

| 实验 | 内容 | 关键图表 |
|------|------|----------|
| 01 CNN原理与实现 | MNIST 卷积神经网络 | 训练曲线、混淆矩阵、Conv1 特征图、分类结果 |
| 02 CNN_NiN | Network in Network 对比 | NiN vs CNN 准确率、Loss 对比、参数量对比 |
| 03 RNN原理与实现 | 时间序列预测 | 原始序列、预测对比、RNN 结构对比、性能对比 |
| 04 RNN-BPTT | 基于时间的反向传播 | 梯度范数、训练曲线对比、激活函数导数 |

## 每个实验文件夹包含

```
实验文件夹/
├── 01_*.png / 02_*.png ...    ← 实验结果图（中文标注）
├── terminal_code.png          ← 代码截图
├── terminal_output.png        ← 终端输出截图
├── execution.log              ← 执行日志
└── results.json               ← 结构化结果数据
```

## 技术栈

| 类别 | 工具 |
|------|------|
| 深度学习 | TensorFlow 2.x, Keras |
| 计算机视觉 | OpenCV 3.4.2 (含 SIFT/xfeatures2d) |
| 机器学习 | scikit-learn 0.23.2 |
| 可视化 | matplotlib 3.3.3 (中文支持) |
| 平台 | SimpleAI 人工智能教学实训系统 |

## Skill 工具集

本仓库附带一个 **Claude Code Skill**（`skill/` 目录），封装了在实验服务器上跑真实实验的完整流水线：

- **`scripts/srv.py`** — 韧性 SSH/SFTP 助手（带重试、断点续传、追加上传）
- **`scripts/terminal_screenshot.py`** — 终端风格截图工具（中文支持、语法高亮）
- **`references/connection.md`** — 三级 SSH 链路故障对策
- **`references/experiment-recipes.md`** — 实验设计配方（怎样让结果有真实实例图）

安装：`cp -r skill/ ~/.claude/skills/shixun-real-experiments/`

详见 [`skill/README.md`](skill/README.md)。

## 关于本仓库

本仓库包含**实验结果与数据**（图表、日志、JSON 结果），以及**实验自动化工具**（skill 目录下的 Python 脚本）。
所有实验在 SimpleAI 平台远程服务器上执行，通过平台 API 和 SSH 完成实验操作与结果采集。

## License

MIT License — 仅供学习参考。
