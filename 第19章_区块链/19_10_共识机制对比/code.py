#!/usr/bin/env python3
"""真实执行源码 — 19_10_共识机制对比"""
def exp_19_10():
    """实验10: 共识机制对比 (PoW/PoS/DPoS)"""
    eid = '19_10_共识机制对比'
    d = exp_start(eid, '共识机制对比')
    files = []

    mechanisms = [
        ('PoW\n工作量证明', '算力竞争\n高能耗', 'Bitcoin\nLitecoin', '#F44336'),
        ('PoS\n权益证明', '持币量决定\n低能耗', 'Ethereum 2.0\nCardano', '#4CAF50'),
        ('DPoS\n委托权益证明', '投票选举\n高TPS', 'EOS\nTRON', '#2196F3'),
        ('PBFT\n实用拜占庭', '投票共识\n低延迟', 'Hyperledger\nTendermint', '#FF9800'),
    ]

    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    for i, (name, desc, examples, color) in enumerate(mechanisms):
        ax = axes[i]
        ax.axis('off')
        ax.set_facecolor(color + '15' if color.startswith('#') else '#f8f8f8')
        ax.text(0.5, 0.8, name, ha='center', fontsize=12, fontproperties=FONT,
                fontweight='bold', color=color, transform=ax.transAxes)
        ax.text(0.5, 0.45, desc, ha='center', fontsize=9, transform=ax.transAxes)
        ax.text(0.5, 0.15, f'代表: {examples}', ha='center', fontsize=8, transform=ax.transAxes, color='#666')

    fig.suptitle('区块链共识机制对比', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_共识机制对比.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'mechanisms': 4})
