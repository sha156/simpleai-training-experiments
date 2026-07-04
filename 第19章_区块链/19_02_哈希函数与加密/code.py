#!/usr/bin/env python3
"""真实执行源码 — 19_02_哈希函数与加密"""
def exp_19_2():
    """实验2: 哈希函数与加密"""
    eid = '19_02_哈希函数与加密'
    d = exp_start(eid, '哈希函数与加密')
    files = []

    # 展示SHA256特性
    msgs = ['Hello', 'hello', 'Hello!', 'Hello World', 'Hello World!']
    hashes = [hashlib.sha256(m.encode()).hexdigest()[:16] + '...' for m in msgs]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 雪崩效应
    s1 = 'Hello World'
    s2 = 'hello World'
    h1 = hashlib.sha256(s1.encode()).hexdigest()
    h2 = hashlib.sha256(s2.encode()).hexdigest()
    diff_bits = sum(bin(int(a,16)^int(b,16)).count('1') for a,b in zip(h1,h2))

    # 哈希分布
    test_hashes = [int(hashlib.sha256(str(i).encode()).hexdigest()[:2], 16) for i in range(200)]

    axes[0].bar(range(len(msgs)), [1]*len(msgs), color=plt.cm.tab10(np.linspace(0,1,len(msgs))))
    for i, (m, h) in enumerate(zip(msgs, hashes)):
        axes[0].text(i, 0.5, f'{m}\n→{h}', ha='center', fontsize=7, fontfamily='monospace')
    axes[0].set_ylim(0, 1.5)
    axes[0].set_title('SHA256 输入 → 哈希 (雪崩效应)', fontproperties=FONT)
    axes[0].axis('off')

    axes[1].hist(test_hashes, bins=20, color='#4CAF50', alpha=0.7)
    axes[1].set_title('哈希值分布 (均匀性)', fontproperties=FONT)
    axes[1].set_xlabel('哈希首2字节')

    fig.suptitle(f'密码学哈希函数 (SHA256)\n"{s1}"→"{s2}" 差异={diff_bits}/256 bits', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_哈希函数.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'hash_bits': 256, 'avalanche': diff_bits})
