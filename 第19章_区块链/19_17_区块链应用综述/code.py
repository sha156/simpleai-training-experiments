#!/usr/bin/env python3
"""真实执行源码 — 19_17_区块链应用综述"""
def exp_19_17():
    eid = '19_17_区块链应用综述'
    d = exp_start(eid, '区块链应用综述')
    files = []
    fig, ax = plt.subplots(figsize=(14, 8)); ax.axis('off')

    apps = [
        ('金融', '跨境支付、DeFi、稳定币、保险', '#2196F3'),
        ('供应链', '溯源、防伪、物流跟踪', '#4CAF50'),
        ('身份认证', 'DID、数字身份、KYC', '#FF9800'),
        ('医疗', '电子病历、药品溯源、数据共享', '#E91E63'),
        ('政务', '电子投票、证书存证、信息公开', '#9C27B0'),
        ('物联网', '设备身份、数据市场、自动结算', '#00BCD4'),
        ('版权', '数字版权、内容变现、IP保护', '#795548'),
    ]

    y = 0.9
    for name, desc, color in apps:
        ax.text(0.1, y, f'◆ {name}', fontsize=12, fontproperties=FONT, fontweight='bold',
                color=color, transform=ax.transAxes)
        ax.text(0.35, y, desc, fontsize=10, transform=ax.transAxes, color='#555')
        y -= 0.12
    ax.set_title('区块链行业应用全景', fontproperties=FONT, fontsize=14)

    p1 = os.path.join(d, '01_区块链应用全景.png'); save_img(fig, p1); files.append(p1)
    exp_done(eid, d, files, {})


# ══════════════════════════════════════════════════════════════
#  主程序
# ══════════════════════════════════════════════════════════════
