#!/usr/bin/env python3
"""真实执行源码 — 19_12_P2P网络"""
def exp_19_12():
    """实验12: P2P网络概念"""
    eid = '19_12_P2P网络'
    d = exp_start(eid, 'P2P网络')
    files = []

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')

    # P2P vs 中心化
    comparison = (
        '               中心化网络                       P2P去中心化网络\n'
        '        ┌──────────────┐              ┌───┐     ┌───┐     ┌───┐\n'
        '        │    ┌───┐     │              │ A │─────│ B │─────│ C │\n'
        '        │    │ A │     │              └─┬─┘     └─┬─┘     └─┬─┘\n'
        '        │    └─┬─┘     │                │    ┌────┘    ┌────┘\n'
        '   ┌──┐ │  ┌───┼───┐  │                │    │    ┌────┘\n'
        '   │C │─┼──┤  Server├──┼──┐           ┌─┴─┐  │  ┌─┴─┐\n'
        '   └──┘ │  └───┼───┘  │  │           │ D │──┴──│ E │\n'
        '         │      │      │  │           └───┘     └───┘\n'
        '         │    ┌─┴─┐    │  │\n'
        '         │    │ B │    │  │           特点:\n'
        '         │    └───┘    │  │           • 所有节点平等\n'
        '         └──────────────┘  │           • 无单点故障\n'
        '                             │           • 容错性强\n'
        '  单点故障, 易审查/攻击      │           • 抗审查\n'
        '                             │\n'
        '  传统的客户端-服务器模型     │           区块链的P2P模型'
    )
    ax.text(0.5, 0.5, comparison, ha='center', va='center', fontsize=8,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#f5f5f5'))
    ax.set_title('P2P网络架构对比', fontproperties=FONT, fontsize=14)

    p1 = os.path.join(d, '01_P2P网络.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})

# 19_13 ~ 19_17: 简化但完整的实验