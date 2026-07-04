#!/usr/bin/env python3
"""真实执行源码 — 05_03_图像直方图"""
def exp_5_3(gray=None):
    """实验3: 图像直方图 - 直方图计算与可视化"""
    eid = '05_03_图像直方图'
    d = exp_start(eid, '图像直方图')
    files = []

    if gray is None:
        gray = load_gray(os.path.join(DATA_CV, 'lena.jpg'))
    if gray is None: gray = load_gray(os.path.join(DATA_CV, 'house.jpg'))
    img_rgb = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))

    # 图1: 灰度直方图 + 累积直方图
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].hist(gray.ravel(), bins=256, range=(0, 255), color='#333333', alpha=0.8)
    axes[0].set_title('灰度直方图', fontproperties=FONT)
    axes[0].set_xlabel('像素值', fontproperties=FONT)
    axes[0].set_ylabel('频数', fontproperties=FONT)

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf / cdf[-1]
    axes[1].plot(cdf_normalized, color='#2196F3', linewidth=2)
    axes[1].set_title('累积分布函数(CDF)', fontproperties=FONT)
    axes[1].set_xlabel('像素值', fontproperties=FONT)
    axes[1].set_ylabel('累积概率', fontproperties=FONT)
    axes[1].set_xlim(0, 255)
    fig.suptitle('图像直方图分析', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_灰�直方图与CDF.png')
    save_img(fig, p1); files.append(p1)

    # 图2: RGB三通道直方图
    if img_rgb is not None:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        colors = ('red', 'green', 'blue')
        for i, color in enumerate(colors):
            hist = cv2.calcHist([img_rgb], [i], None, [256], [0, 256])
            axes[0].plot(hist, color=color, linewidth=1.5, label=f'{color}通道')
        axes[0].legend(prop=FONT)
        axes[0].set_title('RGB三通道直方图', fontproperties=FONT)
        axes[0].set_xlim(0, 255)

        axes[1].imshow(img_rgb)
        axes[1].set_title('原图', fontproperties=FONT)
        axes[1].axis('off')
        fig.suptitle('彩色图像直方图', fontproperties=FONT, fontsize=14)
        fig.tight_layout()
        p2 = os.path.join(d, '02_RGB三通道直方图.png')
        save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'hist_peaks': int(np.argmax(cv2.calcHist([gray],[0],None,[256],[0,256])))})
