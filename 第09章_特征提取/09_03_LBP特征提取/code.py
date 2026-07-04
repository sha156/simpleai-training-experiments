#!/usr/bin/env python3
"""真实执行源码 — 09_03_LBP特征提取"""
def exp_9_3():
    """实验3: LBP特征提取"""
    eid = '09_03_LBP特征提取'
    d = exp_start(eid, 'LBP特征提取')
    files = []

    gray = load_gray(os.path.join(DATA_CV, 'lena.jpg'))

    # LBP实现
    def lbp_basic(img):
        h, w = img.shape
        lbp = np.zeros((h-2, w-2), dtype=np.uint8)
        for i in range(1, h-1):
            for j in range(1, w-1):
                center = img[i, j]
                code = 0
                for k, (di, dj) in enumerate([(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]):
                    if img[i+di, j+dj] >= center:
                        code |= (1 << k)
                lbp[i-1, j-1] = code
        return lbp

    # 用小尺寸加速
    small = cv2.resize(gray, (128, 128))
    lbp_result = lbp_basic(small)

    # 图1: LBP结果
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    axes[0].imshow(gray, cmap='gray'); axes[0].set_title('原图', fontproperties=FONT); axes[0].axis('off')
    axes[1].imshow(small, cmap='gray'); axes[1].set_title('缩放至128×128', fontproperties=FONT); axes[1].axis('off')
    axes[2].imshow(lbp_result, cmap='gray'); axes[2].set_title('LBP特征图', fontproperties=FONT); axes[2].axis('off')
    fig.suptitle('LBP (Local Binary Patterns) 纹理特征', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_LBP特征.png')
    save_img(fig, p1); files.append(p1)

    # 图2: LBP直方图
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].hist(lbp_result.ravel(), bins=256, color='#673AB7', alpha=0.7)
    axes[0].set_title('LBP直方图(256 bins)', fontproperties=FONT)
    axes[0].set_xlim(0, 255)

    # Uniform LBP (简化)
    uniform_hist = np.bincount(lbp_result.ravel(), minlength=256)
    axes[1].bar(range(256), uniform_hist, color='#FF5722', alpha=0.7)
    axes[1].set_title('LBP各模式频数', fontproperties=FONT)
    axes[1].set_xlim(0, 255)

    fig.suptitle('LBP纹理特征统计', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_LBP直方图.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {})
