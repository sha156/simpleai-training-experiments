#!/usr/bin/env python3
"""真实执行源码 — 19_05_区块链创建与验证"""
def exp_19_5():
    """实验5: 区块链创建与验证"""
    eid = '19_05_区块链创建与验证'
    d = exp_start(eid, '区块链创建与验证')
    files = []

    _, Blockchain = blockchain_utils()
    chain = Blockchain(difficulty=2)

    transactions = [
        'Alice → Bob: 50 BTC',
        'Bob → Charlie: 25 BTC',
        'Charlie → Dave: 10 BTC',
        'Dave → Eve: 5 BTC',
        'Alice → Charlie: 30 BTC',
    ]

    for tx in transactions:
        chain.add_block(tx)

    log_print('19.5', f'区块链有效: {chain.is_valid()}')
    log_print('19.5', f'链长度: {len(chain.chain)}')

    # 可视化
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')

    y = 0.95
    for block in chain.chain:
        color = '#4CAF50' if block.index == 0 else '#2196F3'
        ax.text(0.1, y, f'区块#{block.index}: {block.data}', fontsize=9,
                transform=ax.transAxes,
                bbox=dict(facecolor=color, alpha=0.1))
        ax.text(0.75, y, f'哈希: {block.hash[:12]}...', fontsize=8,
                fontfamily='monospace', transform=ax.transAxes, color='#666')
        if block.index > 0:
            ax.annotate('', xy=(0.1, y-0.02), xytext=(0.1, y+0.005),
                       arrowprops=dict(arrowstyle='->', color='#2196F3'))
        y -= 0.14

    vstatus = "✓有效" if chain.is_valid() else "✗无效"
    ax.set_title(f'区块链 ({len(chain.chain)}个区块, 验证: {vstatus})',
                 fontproperties=FONT, fontsize=14)
    p1 = os.path.join(d, '01_区块链.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'chain_length': len(chain.chain), 'valid': chain.is_valid()})
