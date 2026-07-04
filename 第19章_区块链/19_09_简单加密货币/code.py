#!/usr/bin/env python3
"""真实执行源码 — 19_09_简单加密货币"""
def exp_19_9():
    """实验9: 简单加密货币实现"""
    eid = '19_09_简单加密货币'
    d = exp_start(eid, '简单加密货币')
    files = []

    _, Blockchain = blockchain_utils()
    coin = Blockchain(difficulty=2)

    # 模拟交易
    ledger = {}
    transactions = [
        ('Genesis', 'Alice', 100),
        ('Alice', 'Bob', 30),
        ('Alice', 'Charlie', 20),
        ('Bob', 'Dave', 15),
        ('Charlie', 'Eve', 10),
        ('Dave', 'Alice', 5),
    ]

    for sender, receiver, amount in transactions:
        coin.add_block(f'{sender} → {receiver}: {amount} coins')
        ledger[receiver] = ledger.get(receiver, 0) + amount
        if sender != 'Genesis':
            ledger[sender] = ledger.get(sender, 0) - amount

    # 图: 账本可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    people = list(ledger.keys())
    balances = [ledger[p] for p in people]
    colors = plt.cm.tab10(np.linspace(0, 1, len(people)))
    axes[0].bar(people, balances, color=colors, alpha=0.8)
    for i, (p, b) in enumerate(zip(people, balances)):
        axes[0].text(i, b + 1, str(b), ha='center', fontsize=10)
    axes[0].set_title('账户余额', fontproperties=FONT)
    axes[0].set_ylabel('coin', fontproperties=FONT)

    # 交易图
    axes[1].axis('off')
    tx_text = '\n'.join([f'{i}. {s} → {r}: {a}' for i, (s, r, a) in enumerate(transactions)])
    axes[1].text(0.5, 0.5, tx_text, ha='center', va='center', fontsize=10,
                 fontfamily='monospace', transform=axes[1].transAxes,
                 bbox=dict(boxstyle='round', facecolor='#f0f0f0'))
    axes[1].set_title('交易记录', fontproperties=FONT)

    coin_valid = "✓" if coin.is_valid() else "✗"
    fig.suptitle(f'简单加密货币 (链长={len(coin.chain)}, 有效={coin_valid})',
                 fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_加密货币.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'transactions': len(transactions), 'valid': coin.is_valid()})
