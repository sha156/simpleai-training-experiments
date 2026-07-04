#!/usr/bin/env python3
"""真实执行源码 — 19_14_以太坊与Gas"""
def exp_19_14():
    eid = '19_14_以太坊与Gas'
    d = exp_start(eid, '以太坊与Gas')
    files = []
    fig, ax = plt.subplots(figsize=(12, 7)); ax.axis('off')
    gas = (
        '        以太坊 Gas 机制\n\n'
        '  操作           Gas消耗      说明\n'
        '  ─────────────────────────────────\n'
        '  简单转账      21,000        ETH转账\n'
        '  ERC20转账     45,000-65,000 代币转账\n'
        '  Uniswap交易   150,000+     DEX交易\n'
        '  合约部署      200,000+     新合约\n'
        '  NFT铸造       100,000-300,000\n\n'
        '  Gas Price × Gas Used = 交易费 (ETH)\n'
        '  EIP-1559: Base Fee + Priority Fee'
    )
    ax.text(0.5, 0.5, gas, ha='center', va='center', fontsize=9,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#E8EAF6'))
    ax.set_title('以太坊Gas机制', fontproperties=FONT, fontsize=14)
    p1 = os.path.join(d, '01_以太坊Gas.png'); save_img(fig, p1); files.append(p1)
    exp_done(eid, d, files, {})
