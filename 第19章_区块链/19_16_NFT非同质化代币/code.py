#!/usr/bin/env python3
"""真实执行源码 — 19_16_NFT非同质化代币"""
def exp_19_16():
    eid = '19_16_NFT非同质化代币'
    d = exp_start(eid, 'NFT非同质化代币')
    files = []
    fig, ax = plt.subplots(figsize=(12, 7)); ax.axis('off')
    nft = (
        '        NFT (非同质化代币) - ERC-721标准\n\n'
        '  FT (同质化): 1 ETH = 1 ETH, 可互换\n'
        '  NFT (非同质化): 每个token独一无二\n\n'
        '  应用场景:\n'
        '  • 数字艺术 (Beeple, PAK)\n'
        '  • 游戏资产 (Axie Infinity)\n'
        '  • 虚拟土地 (Decentraland, Sandbox)\n'
        '  • 音乐/视频/域名\n'
        '  • 身份认证/文凭证书\n\n'
        '  ERC-721: tokenId + metadata URI → 链上唯一\n'
        '  ERC-1155: 半同质化 (批量铸造, 节省Gas)'
    )
    ax.text(0.5, 0.5, nft, ha='center', va='center', fontsize=9,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#F3E5F5'))
    ax.set_title('NFT非同质化代币', fontproperties=FONT, fontsize=14)
    p1 = os.path.join(d, '01_NFT.png'); save_img(fig, p1); files.append(p1)
    exp_done(eid, d, files, {})
