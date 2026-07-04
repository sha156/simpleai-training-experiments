#!/usr/bin/env python3
"""真实执行源码 — 16_04_马尔可夫随机场去噪"""
def exp_16_4():
    """实验4: 马尔可夫随机场与图像去噪"""
    eid = '16_04_马尔可夫随机场去噪'
    d = exp_start(eid, 'MRF图像去噪')
    files = []

    import cv2
    gray = cv2.imread(os.path.join(DATA_CV, 'lena.jpg'), 0)
    if gray is None:
        gray = np.random.randint(0, 255, (128, 128), dtype=np.uint8)
    gray_small = cv2.resize(gray, (64, 64))

    # 添加椒盐噪声
    noisy = gray_small.copy()
    noise_mask = np.random.random(noisy.shape) < 0.15
    noisy[noise_mask] = np.random.choice([0, 255], size=np.sum(noise_mask))

    # 简单MRF去噪 (ICM/Graph Cut的简化版)
    def mrf_denoise(img, n_iter=5, beta=1.0):
        h, w = img.shape
        denoised = img.copy().astype(np.float64)
        for _ in range(n_iter):
            new = denoised.copy()
            for i in range(1, h-1):
                for j in range(1, w-1):
                    neighbors = np.array([
                        denoised[i-1, j], denoised[i+1, j],
                        denoised[i, j-1], denoised[i, j+1]
                    ])
                    data_term = (denoised[i, j] - img[i, j]) ** 2
                    smooth_term = beta * np.sum((denoised[i, j] - neighbors) ** 2)
                    # 尝试两个候选值: 保持原值或邻域均值
                    candidates = [denoised[i, j], np.mean(neighbors)]
                    costs = [(c - img[i, j])**2 + beta * np.sum((c - neighbors)**2) for c in candidates]
                    new[i, j] = candidates[np.argmin(costs)]
            denoised = new
        return np.clip(denoised, 0, 255).astype(np.uint8)

    denoised = mrf_denoise(noisy, n_iter=5, beta=0.5)

    # 中值滤波对比
    median_denoised = cv2.medianBlur(noisy, 3)

    # 图1
    fig = make_montage(
        [gray_small, noisy, denoised, median_denoised],
        ['原图', f'椒盐噪声(15%)', 'MRF去噪', '中值滤波去噪'],
        cols=4, figsize=(18, 5),
        main_title='马尔可夫随机场(MRF)图像去噪'
    )
    p1 = os.path.join(d, '01_MRF去噪.png')
    save_img(fig, p1); files.append(p1)

    # 图2: PSNR对比
    from math import log10
    def psnr(original, degraded):
        mse = np.mean((original.astype(float) - degraded.astype(float))**2)
        if mse == 0: return 100
        return 20 * log10(255.0 / np.sqrt(mse))

    methods = {'原噪图': noisy, 'MRF去噪': denoised, '中值滤波': median_denoised}
    psnrs = {k: psnr(gray_small, v) for k, v in methods.items()}

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#F44336', '#4CAF50', '#2196F3']
    for i, (name, val) in enumerate(psnrs.items()):
        ax.bar(i, val, color=colors[i], alpha=0.8)
        ax.text(i, val + 0.3, f'{val:.1f}dB', ha='center', fontsize=12)
    ax.set_xticks(range(3)); ax.set_xticklabels(list(psnrs.keys()), fontproperties=FONT)
    ax.set_title('去噪效果对比 (PSNR)', fontproperties=FONT, fontsize=14)
    ax.set_ylabel('PSNR (dB)', fontproperties=FONT)
    fig.tight_layout()
    p2 = os.path.join(d, '02_去噪PSNR对比.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, psnrs)


# ══════════════════════════════════════════════════════════════
#  第17章: 机器学习图像处理 (6个实验)
# ══════════════════════════════════════════════════════════════
