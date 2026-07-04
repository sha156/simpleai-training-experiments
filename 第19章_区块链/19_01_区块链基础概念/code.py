#!/usr/bin/env python3
"""真实执行源码 — 19_01_区块链基础概念"""
def exp_19_1():
    """实验1: 区块链基础概念"""
    eid = '19_01_区块链基础概念'
    d = exp_start(eid, '区块链基础概念')
    files = []

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')

    concept = (
        '                    区块链核心概念\n\n'
        '  ┌───────────────────────────────────────────────┐\n'
        '  │  区块 N-1          区块 N          区块 N+1     │\n'
        '  │  ┌─────────┐      ┌─────────┐      ┌─────────┐ │\n'
        '  │  │ 数据     │      │ 数据     │      │ 数据     │ │\n'
        '  │  │ 时间戳   │      │ 时间戳   │      │ 时间戳   │ │\n'
        '  │  │ 前一哈希  │←────│ 前一哈希  │←────│ 前一哈希  │ │\n'
        '  │  │ 本区块哈希│     │ 本区块哈希│     │ 本区块哈希│ │\n'
        '  │  └─────────┘      └─────────┘      └─────────┘ │\n'
        '  └───────────────────────────────────────────────┘\n\n'
        '  关键特性:\n'
        '  • 去中心化: 无单一控制节点, P2P网络\n'
        '  • 不可篡改: 每个区块通过哈希链接\n'
        '  • 透明可审计: 所有交易公开可查\n'
        '  • 共识机制: PoW/PoS/DPoS/BFT\n'
        '  • 智能合约: 自动执行的代码逻辑'
    )
    ax.text(0.5, 0.5, concept, ha='center', va='center', fontsize=9,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#E8EAF6'))
    ax.set_title('区块链核心概念', fontproperties=FONT, fontsize=14)
    p1 = os.path.join(d, '01_区块链概念.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})
