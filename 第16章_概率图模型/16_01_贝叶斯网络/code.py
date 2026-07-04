#!/usr/bin/env python3
"""真实执行源码 — 16_01_贝叶斯网络"""
def fix_16_01():
    """贝叶斯网络"""
    d = OUT_DIRS[4]
    files = []

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    concept = (
        '                    贝叶斯网络 (Bayesian Network)\n\n'
        '  ┌──────────────────────────────────────────────────┐\n'
        '  │                                                  │\n'
        '  │       下雨 P(R)=0.2                              │\n'
        '  │         │    ＼                                   │\n'
        '  │         ↓      ↓                                  │\n'
        '  │    洒水器    草地湿                               │\n'
        '  │  P(S|R)=0.01  P(W|R,S)=0.99                      │\n'
        '  │  P(S|¬R)=0.4  P(W|R,¬S)=0.8                      │\n'
        '  │               P(W|¬R,S)=0.9                       │\n'
        '  │               P(W|¬R,¬S)=0.0                      │\n'
        '  │                                                  │\n'
        '  │  推理示例:                                       │\n'
        '  │  已知草地湿了 → 下雨概率?                        │\n'
        '  │  P(R|W) = P(W|R)P(R) / P(W)                      │\n'
        '  │         = 0.2*P(W|R) / P(W)                      │\n'
        '  │                                                  │\n'
        '  │  特点: 有向无环图(DAG) + 条件概率表(CPT)         │\n'
        '  └──────────────────────────────────────────────────┘'
    )
    ax.text(0.5, 0.5, concept, ha='center', va='center', fontsize=10,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#E3F2FD'))
    ax.set_title('贝叶斯网络 — 洒水器模型', fontproperties=FONT, fontsize=14)
    p = os.path.join(d, '01_贝叶斯网络.png')
    save_img(fig, p); files.append(p)

    # 条件概率可视化
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    axes[0].bar(['下雨','不下雨'], [0.2, 0.8], color=['#2196F3','#FF9800'])
    axes[0].set_title('P(Rain) 先验', fontproperties=FONT)
    conditions = ['R,S', 'R,¬S', '¬R,S', '¬R,¬S']
    axes[1].bar(conditions, [0.99, 0.8, 0.9, 0.0], color=plt.cm.RdYlGn([0.1,0.3,0.6,0.9]))
    axes[1].set_title('P(Wet|Rain,Sprinkler)', fontproperties=FONT)
    axes[1].tick_params(rotation=30)
    axes[2].bar(['无证据','草湿→P(雨)'], [0.2, 0.64], color=['#888','#4CAF50'])
    axes[2].set_title('贝叶斯推断', fontproperties=FONT)
    fig.tight_layout()
    p2 = os.path.join(d, '02_贝叶斯推理.png')
    save_img(fig, p2); files.append(p2)

    with open(os.path.join(d, 'results.json'), 'w') as f:
        json.dump({'files': files}, f)
    print(f'16_01: {len(files)} files OK')
