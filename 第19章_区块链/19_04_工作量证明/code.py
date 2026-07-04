#!/usr/bin/env python3
"""真实执行源码 — 19_04_工作量证明"""
def exp_19_4():
    """实验4: 工作量证明(PoW)"""
    eid = '19_04_工作量证明'
    d = exp_start(eid, '工作量证明')
    files = []

    # 不同难度下的挖矿次数
    difficulties = range(1, 6)
    nonces = []
    for diff in difficulties:
        block = hashlib.sha256(b'test').hexdigest()
        nonce = 0
        target = '0' * diff
        while True:
            h = hashlib.sha256(f'{block}{nonce}'.encode()).hexdigest()
            if h[:diff] == target:
                nonces.append(nonce)
                break
            nonce += 1
            if nonce > 500000:
                nonces.append(nonce)
                break

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].bar(list(difficulties), nonces, color=plt.cm.Reds(np.linspace(0.3, 0.9, len(difficulties))))
    axes[0].set_title('难度 vs 挖矿尝试次数', fontproperties=FONT)
    axes[0].set_xlabel('难度 (前导零个数)'); axes[0].set_ylabel('尝试次数')
    axes[0].set_yscale('log')

    axes[1].plot(list(difficulties), [2**d for d in difficulties], 'r--', label='理论: 2^d')
    axes[1].plot(list(difficulties), nonces, 'b-o', label='实测nonce')
    axes[1].set_title('实测 vs 理论期望', fontproperties=FONT)
    axes[1].set_xlabel('难度'); axes[1].set_yscale('log')
    axes[1].legend(prop=FONT)

    fig.suptitle('工作量证明 (Proof of Work)', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_PoW工作量证明.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'difficulties': list(difficulties), 'nonces': nonces})
