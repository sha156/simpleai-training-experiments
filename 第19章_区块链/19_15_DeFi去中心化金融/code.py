#!/usr/bin/env python3
"""真实执行源码 — 19_15_DeFi去中心化金融"""
def exp_19_15():
    eid = '19_15_DeFi去中心化金融'
    d = exp_start(eid, 'DeFi去中心化金融')
    files = []
    fig, ax = plt.subplots(figsize=(14, 8)); ax.axis('off')
    defi = (
        '              DeFi (去中心化金融) 生态\n\n'
        '  ┌──────────────────────────────────────────────┐\n'
        '  │  DEX (去中心化交易所)  Lending (借贷)          │\n'
        '  │  Uniswap / SushiSwap    Aave / Compound        │\n'
        '  │                                              │\n'
        '  │  Stablecoins (稳定币)   Derivatives (衍生品)   │\n'
        '  │  DAI / USDC / USDT      dYdX / Synthetix      │\n'
        '  │                                              │\n'
        '  │  Yield (收益聚合)       Insurance (保险)       │\n'
        '  │  Yearn / Convex         Nexus Mutual           │\n'
        '  └──────────────────────────────────────────────┘\n\n'
        '  TVL (总锁仓量) 趋势: 持续增长\n'
        '  核心优势: 无需许可 / 透明 / 可组合'
    )
    ax.text(0.5, 0.5, defi, ha='center', va='center', fontsize=9,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#E8F5E9'))
    ax.set_title('DeFi去中心化金融生态', fontproperties=FONT, fontsize=14)
    p1 = os.path.join(d, '01_DeFi生态.png'); save_img(fig, p1); files.append(p1)
    exp_done(eid, d, files, {})
