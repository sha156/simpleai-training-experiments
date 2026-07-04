#!/usr/bin/env python3
"""真实执行源码 — 19_07_默克尔树"""
def exp_19_7():
    """实验7: 默克尔树 (Merkle Tree)"""
    eid = '19_07_默克尔树'
    d = exp_start(eid, '默克尔树')
    files = []

    # 构建简单默克尔树
    transactions = [f'Tx{i}' for i in range(8)]
    leaves = [hashlib.sha256(tx.encode()).hexdigest() for tx in transactions]

    tree_levels = [leaves]
    current = leaves
    while len(current) > 1:
        if len(current) % 2 == 1:
            current.append(current[-1])
        next_level = []
        for i in range(0, len(current), 2):
            combined = current[i] + current[i+1]
            next_level.append(hashlib.sha256(combined.encode()).hexdigest())
        tree_levels.append(next_level)
        current = next_level

    # 图: 默克尔树
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')

    for level_idx, level in enumerate(tree_levels):
        y = 0.9 - level_idx * 0.25
        for node_idx, node_hash in enumerate(level):
            x = 0.1 + node_idx * (0.8 / (len(level) - 1)) if len(level) > 1 else 0.5
            ax.text(x, y, node_hash[:8] + '...', ha='center', fontsize=7,
                    fontfamily='monospace',
                    bbox=dict(facecolor='#E3F2FD', edgecolor='#2196F3', boxstyle='round'),
                    transform=ax.transAxes)
            if level_idx < len(tree_levels) - 1:
                child_y = y - 0.22
                for child_offset in [0, 1]:
                    child_idx = node_idx * 2 + child_offset
                    if child_idx < len(tree_levels[level_idx + 1]):
                        child_x = 0.1 + child_idx * (0.8 / (len(tree_levels[level_idx+1]) - 1)) if len(tree_levels[level_idx+1]) > 1 else 0.5
                        ax.plot([x, child_x], [y-0.03, child_y+0.03], 'b-', linewidth=0.5,
                                transform=ax.transAxes)

    ax.set_title('默克尔树 (Merkle Tree) - 8笔交易', fontproperties=FONT, fontsize=14)
    p1 = os.path.join(d, '01_默克尔树.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'n_transactions': 8, 'tree_height': len(tree_levels)})
