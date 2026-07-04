#!/usr/bin/env python3
"""真实执行源码 — 16_03_条件随机场"""
def exp_16_3():
    """实验3: 条件随机场(CRF)基础"""
    eid = '16_03_条件随机场'
    d = exp_start(eid, '条件随机场')
    files = []

    # CRF用于序列标注的可视化
    # 模拟命名实体识别
    np.random.seed(42)

    # 图1: CRF vs HMM 对比
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    for ax, (title, model_type) in zip(axes, [('HMM生成模型', 'hmm'), ('CRF判别模型', 'crf')]):
        ax.axis('off')
        ax.set_title(title, fontproperties=FONT, fontsize=12)
        if model_type == 'hmm':
            desc = 'P(X,Y) = P(Y₁)∏P(Yᵗ|Yᵗ⁻¹)∏P(Xᵗ|Yᵗ)\n\n生成模型：\n建模联合概率分布\n假设观测独立'
        else:
            desc = 'P(Y|X) = exp(ΣλⱼFⱼ(Y,X)) / Z(X)\n\n判别模型：\n直接建模条件概率\n可引入任意特征'
        ax.text(0.5, 0.5, desc, ha='center', va='center', fontsize=10,
                transform=ax.transAxes, fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='#f5f5f5'))

    fig.suptitle('序列标注模型对比: HMM vs CRF', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_CRF_vs_HMM.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 模拟序列标注结果
    tokens = ['张', '三', '在', '北京', '大学', '读书']
    labels = ['B-PER', 'I-PER', 'O', 'B-ORG', 'I-ORG', 'O']

    fig, ax = plt.subplots(figsize=(12, 4))
    colors_map = {'B-PER': '#FF6B6B', 'I-PER': '#FF8E8E', 'B-ORG': '#4ECDC4', 'I-ORG': '#7EDDD6', 'O': '#DDDDDD'}
    for i, (tok, lab) in enumerate(zip(tokens, labels)):
        ax.text(i, 0.6, tok, ha='center', fontsize=16, fontproperties=FONT)
        ax.text(i, 0.3, lab, ha='center', fontsize=10, fontproperties=FONT,
                bbox=dict(facecolor=colors_map.get(lab, '#DDD'), alpha=0.6))
    ax.set_xlim(-0.5, len(tokens) - 0.5)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('CRF命名实体识别示例', fontproperties=FONT, fontsize=14)
    p2 = os.path.join(d, '02_NER示例.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'labels': ['B-PER','I-PER','B-ORG','I-ORG','O']})
