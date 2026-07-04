#!/usr/bin/env python3
"""真实执行源码 — 19_03_区块结构"""
def exp_19_3():
    """实验3: 区块结构"""
    eid = '19_03_区块结构'
    d = exp_start(eid, '区块结构')
    files = []

    Block, _ = blockchain_utils()

    # 创建并可视化区块
    block = Block(1, time.time(), 'Alice → Bob: 100 BTC', '0'*64)
    block.mine_block(difficulty=3)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')

    block_info = (
        f'  区块 #{block.index}\n'
        f'  ┌──────────────────────────────────────┐\n'
        f'  │  时间戳: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(block.timestamp))}\n'
        f'  │  数据:    {block.data}\n'
        f'  │  前哈希:  {block.previous_hash[:32]}...\n'
        f'  │  本哈希:  {block.hash[:32]}...\n'
        f'  │  Nonce:   {block.nonce}\n'
        f'  │  挖矿次数: {block.nonce} 次尝试\n'
        f'  └──────────────────────────────────────┘'
    )
    ax.text(0.5, 0.5, block_info, ha='center', va='center', fontsize=10,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#E3F2FD'))
    ax.set_title('区块结构详解', fontproperties=FONT, fontsize=14)
    p1 = os.path.join(d, '01_区块结构.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'block_index': 1, 'nonce': block.nonce, 'hash_prefix': block.hash[:10]})
