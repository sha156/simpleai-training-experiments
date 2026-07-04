#!/usr/bin/env python3
"""真实执行源码 — 19_08_数字签名"""
def exp_19_8():
    """实验8: 数字签名 (ECDSA)"""
    eid = '19_08_数字签名'
    d = exp_start(eid, '数字签名')
    files = []

    # 演示数字签名流程
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')

    flow = (
        '                    数字签名流程 (ECDSA)\n\n'
        '  ┌──────────────────────────────────────────────────────┐\n'
        '  │  签名过程 (Sign)                  验证过程 (Verify)    │\n'
        '  │                                                       │\n'
        '  │  1. 生成密钥对                     1. 收到消息+签名     │\n'
        '  │     privateKey, publicKey          2. 用发送方公钥     │\n'
        '  │                                    3. 重新计算哈希     │\n'
        '  │  2. 计算消息哈希                   4. 验证签名匹配     │\n'
        '  │     hash = SHA256(msg)                                  │\n'
        '  │                                    if verify(publicKey, │\n'
        '  │  3. 用私钥签名                        hash, signature):│\n'
        '  │     sig = ECDSA_sign(              → ✓ 消息未被篡改   │\n'
        '  │           privateKey, hash)            且来自正确发送方 │\n'
        '  │  ─────────────────────────────────────────────────────  │\n'
        '  │  核心: 只有拥有私钥的人才能签名;                        │\n'
        '  │        任何人都可以用公钥验证签名                       │\n'
        '  └──────────────────────────────────────────────────────┘'
    )
    ax.text(0.5, 0.5, flow, ha='center', va='center', fontsize=9,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#FFF8E1'))
    ax.set_title('数字签名原理 (ECDSA)', fontproperties=FONT, fontsize=14)

    p1 = os.path.join(d, '01_数字签名.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})
