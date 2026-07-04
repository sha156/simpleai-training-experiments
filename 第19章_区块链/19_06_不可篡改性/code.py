#!/usr/bin/env python3
"""真实执行源码 — 19_06_不可篡改性"""
def exp_19_6():
    """实验6: 区块链不可篡改性验证"""
    eid = '19_06_不可篡改性'
    d = exp_start(eid, '不可篡改性')
    files = []

    _, Blockchain = blockchain_utils()
    chain = Blockchain(difficulty=2)
    for tx in ['tx1', 'tx2', 'tx3', 'tx4']:
        chain.add_block(tx)

    valid_before = chain.is_valid()

    # 篡改
    chain.chain[2].data = 'HACKED: steal all BTC'
    valid_after = chain.is_valid()

    # 图
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].axis('off')
    axes[0].text(0.5, 0.7, '篡改前', ha='center', fontsize=14, fontproperties=FONT, fontweight='bold',
                transform=axes[0].transAxes)
    axes[0].text(0.5, 0.5, f'区块2数据: "tx2"\n链验证: {"✓ 有效" if valid_before else "✗ 无效"}',
                ha='center', fontsize=12, transform=axes[0].transAxes,
                bbox=dict(facecolor='#E8F5E9'))

    axes[1].axis('off')
    axes[1].text(0.5, 0.7, '篡改后', ha='center', fontsize=14, fontproperties=FONT, fontweight='bold',
                color='red', transform=axes[1].transAxes)
    axes[1].text(0.5, 0.5, f'区块2数据: "HACKED: ..."\n链验证: {"✓ 有效" if valid_after else "✗ 无效"}\n\n原因: 区块2哈希变了\n→区块3的前哈希对不上',
                ha='center', fontsize=11, transform=axes[1].transAxes,
                bbox=dict(facecolor='#FFEBEE'))

    fig.suptitle('区块链不可篡改性验证', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_不可篡改性.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'valid_before': valid_before, 'valid_after': valid_after})
