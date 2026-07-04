#!/usr/bin/env python3
"""真实执行源码 — 19_13_UTXO模型"""
def exp_19_13():
    eid = '19_13_UTXO模型'
    d = exp_start(eid, 'UTXO模型')
    files = []
    fig, ax = plt.subplots(figsize=(12, 7)); ax.axis('off')
    utxo = (
        '        UTXO (Unspent Transaction Output) 模型\n\n'
        '  Alice有100 BTC (来自之前交易的输出)\n'
        '  Alice → Bob 30 BTC:\n'
        '    Input: Alice的100 BTC UTXO\n'
        '    Output: Bob 30 BTC (新UTXO)\n'
        '            Alice 70 BTC (找零, 新UTXO)\n\n'
        '  特点: 每笔交易消费旧UTXO, 产生新UTXO\n'
        '        余额 = 所有属于该地址的UTXO之和'
    )
    ax.text(0.5, 0.5, utxo, ha='center', va='center', fontsize=10,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#FFF3E0'))
    ax.set_title('UTXO交易模型', fontproperties=FONT, fontsize=14)
    p1 = os.path.join(d, '01_UTXO模型.png'); save_img(fig, p1); files.append(p1)
    exp_done(eid, d, files, {})
