#!/usr/bin/env python3
"""真实执行源码 — 16_02_隐马尔可夫模型"""
def exp_16_2():
    """实验2: 隐马尔可夫模型(HMM)"""
    eid = '16_02_隐马尔可夫模型'
    d = exp_start(eid, '隐马尔可夫模型')
    files = []

    # HMM实现: 天气(隐状态) -> 活动(观测)
    # 隐状态: Sunny(0), Rainy(1)
    # 观测: Walk(0), Shop(1), Clean(2)
    np.random.seed(42)

    # 转移矩阵
    trans = np.array([[0.7, 0.3], [0.4, 0.6]])
    # 发射矩阵
    emit = np.array([[0.6, 0.3, 0.1], [0.1, 0.4, 0.5]])
    # 初始概率
    start = np.array([0.6, 0.4])

    # 生成序列
    def generate_sequence(n_steps=200):
        states = [np.random.choice(2, p=start)]
        obs = [np.random.choice(3, p=emit[states[-1]])]
        for _ in range(n_steps - 1):
            states.append(np.random.choice(2, p=trans[states[-1]]))
            obs.append(np.random.choice(3, p=emit[states[-1]]))
        return np.array(states), np.array(obs)

    states, obs = generate_sequence(200)

    # 图1: HMM示意
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))

    axes[0].plot(states[:100], 'b-', linewidth=1, alpha=0.7, drawstyle='steps-post')
    axes[0].set_yticks([0, 1])
    axes[0].set_yticklabels(['晴天', '雨天'], fontproperties=FONT)
    axes[0].set_title('隐状态序列 (前100步)', fontproperties=FONT)
    axes[0].set_xlabel('时间步')

    axes[1].plot(obs[:100], 'r-', linewidth=1, alpha=0.7, drawstyle='steps-post')
    axes[1].set_yticks([0, 1, 2])
    axes[1].set_yticklabels(['散步', '购物', '打扫'], fontproperties=FONT)
    axes[1].set_title('观测序列 (前100步)', fontproperties=FONT)
    axes[1].set_xlabel('时间步')

    fig.suptitle('隐马尔可夫模型 (HMM): 天气→活动', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_HMM序列.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 转移与发射矩阵
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    im1 = axes[0].imshow(trans, cmap='Blues')
    for i in range(2):
        for j in range(2):
            axes[0].text(j, i, f'{trans[i,j]:.1f}', ha='center', va='center', fontsize=14,
                        color='white' if trans[i,j] > 0.5 else 'black')
    axes[0].set_xticks([0,1]); axes[0].set_yticks([0,1])
    axes[0].set_xticklabels(['晴天', '雨天'], fontproperties=FONT)
    axes[0].set_yticklabels(['晴天', '雨天'], fontproperties=FONT)
    axes[0].set_title('状态转移矩阵', fontproperties=FONT)

    im2 = axes[1].imshow(emit, cmap='Greens')
    for i in range(2):
        for j in range(3):
            axes[1].text(j, i, f'{emit[i,j]:.1f}', ha='center', va='center', fontsize=14,
                        color='white' if emit[i,j] > 0.5 else 'black')
    axes[1].set_xticks([0,1,2]); axes[1].set_yticks([0,1])
    axes[1].set_xticklabels(['散步', '购物', '打扫'], fontproperties=FONT)
    axes[1].set_yticklabels(['晴天', '雨天'], fontproperties=FONT)
    axes[1].set_title('发射矩阵', fontproperties=FONT)

    fig.suptitle('HMM参数', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_HMM参数.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'n_states': 2, 'n_observations': 3, 'sequence_length': 200})
