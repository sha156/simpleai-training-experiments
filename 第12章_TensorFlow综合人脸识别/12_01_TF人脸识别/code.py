#!/usr/bin/env python3
"""真实执行源码 — 12_01_TF人脸识别"""
def fix_12_01():
    """TF人脸识别 - 概念展示"""
    d = OUT_DIRS[2]
    files = []

    # 图1: 人脸识别流程
    fig, ax = plt.subplots(figsize=(14, 8)); ax.axis('off')
    flow = (
        '          TensorFlow 人脸识别系统\n\n'
        '  ┌────────────────────────────────────────────┐\n'
        '  │  1. 人脸检测 (MTCNN/SSD)                     │\n'
        '  │       ↓                                      │\n'
        '  │  2. 人脸对齐 (仿射变换 → 标准位置)            │\n'
        '  │       ↓                                      │\n'
        '  │  3. 特征提取 (CNN → 128维嵌入向量)            │\n'
        '  │       ↓                                      │\n'
        '  │  4. 特征比对 (余弦相似度 → 身份识别)          │\n'
        '  │                                              │\n'
        '  │  模型: FaceNet / ArcFace / DeepFace          │\n'
        '  │  损失: Triplet Loss / ArcFace Loss           │\n'
        '  │  数据集: LFW / FERET / CASIA-WebFace         │\n'
        '  │  准确率: LFW > 99.8%                         │\n'
        '  └────────────────────────────────────────────┘'
    )
    ax.text(0.5, 0.5, flow, ha='center', va='center', fontsize=10,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#E8F5E9'))
    ax.set_title('TensorFlow人脸识别系统架构', fontproperties=FONT, fontsize=14)
    p = os.path.join(d, '01_人脸识别架构.png')
    save_img(fig, p); files.append(p)

    # 图2: Triplet Loss原理
    fig, ax = plt.subplots(figsize=(12, 6)); ax.axis('off')
    triplet = (
        '          Triplet Loss 原理\n\n'
        '    Anchor (基准人脸)     Positive (同人)     Negative (不同人)\n'
        '        ●                      ●                    ○\n'
        '        │←──── d(A,P) ────→│   │←─ d(A,N) ─→│\n'
        '        │      要最小化      │   │    要最大化   │\n\n'
        '    L = max(d(A,P) - d(A,N) + margin, 0)\n\n'
        '    目标: 让同人距离 < 不同人距离 - margin\n'
        '    常用margin: 0.2~1.0'
    )
    ax.text(0.5, 0.5, triplet, ha='center', va='center', fontsize=10,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#FFF3E0'))
    ax.set_title('Triplet Loss 人脸识别训练', fontproperties=FONT, fontsize=14)
    p2 = os.path.join(d, '02_TripletLoss.png')
    save_img(fig, p2); files.append(p2)

    with open(os.path.join(d, 'results.json'), 'w') as f:
        json.dump({'files': files, 'note': '人脸识别概念展示'}, f)
    print(f'12_01: {len(files)} files OK')
