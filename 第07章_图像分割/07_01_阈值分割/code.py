#!/usr/bin/env python3
"""真实执行源码 — 07_01_阈值分割"""
def exp_7_1():
    """实验1: 阈值分割 - 全局/自适应/Otsu"""
    eid = '07_01_阈值分割'
    d = exp_start(eid, '阈值分割')
    files = []

    gray = load_gray(os.path.join(DATA_CV, 'lena.jpg'))
    gray2 = load_gray(os.path.join(DATA_CV, 'Lincoln.png'))

    for name, g in [('lena', gray), ('Lincoln', gray2)]:
        if g is None: continue

        # 全局阈值
        _, binary = cv2.threshold(g, 127, 255, cv2.THRESH_BINARY)
        _, binary_inv = cv2.threshold(g, 127, 255, cv2.THRESH_BINARY_INV)
        _, trunc = cv2.threshold(g, 127, 255, cv2.THRESH_TRUNC)

        # Otsu
        _, otsu = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 自适应阈值
        adap_mean = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        adap_gauss = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        fig = make_montage(
            [g, binary, binary_inv, otsu, adap_mean, adap_gauss],
            ['原图(灰度)', '全局阈值127', '反二值化', 'Otsu自动阈值', '自适应均值', '自适应高斯'],
            cols=3, figsize=(16, 10),
            main_title=f'阈值分割方法对比 — {name}'
        )
        p = os.path.join(d, f'01_阈值分割_{name}.png')
        save_img(fig, p); files.append(p)

    # 图2: 不同阈值对比
    if gray is not None:
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        for i, th in enumerate([30, 60, 90, 120, 150, 180, 210, 240]):
            ax = axes[i//4, i%4]
            _, bw = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY)
            ax.imshow(bw, cmap='gray')
            ax.set_title(f'阈值={th}', fontproperties=FONT)
            ax.axis('off')
        fig.suptitle('不同二值化阈值效果', fontproperties=FONT, fontsize=14)
        fig.tight_layout()
        p2 = os.path.join(d, '02_不同阈值对比.png')
        save_img(fig, p2); files.append(p2)

    # 图3: 直方图+OTSU阈值
    if gray is not None:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(gray.ravel(), bins=256, range=(0,255), color='#888', alpha=0.7)
        otsu_thresh, _ = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        ax.axvline(otsu_thresh, color='red', linestyle='--', linewidth=2, label=f'Otsu阈值={otsu_thresh}')
        ax.axvline(127, color='blue', linestyle=':', linewidth=2, label='mid阈值=127')
        ax.legend(prop=FONT)
        ax.set_title('直方图与分割阈值', fontproperties=FONT)
        ax.set_xlim(0, 255)
        fig.tight_layout()
        p3 = os.path.join(d, '03_直方图与Otsu阈值.png')
        save_img(fig, p3); files.append(p3)

    exp_done(eid, d, files, {})
