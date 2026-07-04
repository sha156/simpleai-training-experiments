#!/usr/bin/env python3
"""真实执行源码 — 09_04_颜色直方图特征"""
def exp_9_4():
    """实验4: 颜色直方图特征"""
    eid = '09_04_颜色直方图特征'
    d = exp_start(eid, '颜色直方图特征')
    files = []

    imgs, names = get_real_images(6)

    # 图1: 6图颜色直方图对比
    fig, axes = plt.subplots(3, 4, figsize=(18, 12))
    for i in range(min(6, len(imgs))):
        row = i // 2
        # 显示原图
        axes[row, i%2*2].imshow(imgs[i])
        axes[row, i%2*2].set_title(names[i], fontproperties=FONT, fontsize=9)
        axes[row, i%2*2].axis('off')
        # 显示RGB直方图
        colors = ('red', 'green', 'blue')
        for c_idx, color in enumerate(colors):
            hist = cv2.calcHist([imgs[i]], [c_idx], None, [256], [0, 256])
            axes[row, i%2*2+1].plot(hist, color=color, linewidth=1)
        axes[row, i%2*2+1].set_title(f'{names[i]} RGB直方图', fontproperties=FONT, fontsize=9)
        axes[row, i%2*2+1].set_xlim(0, 256)

    # 隐藏多余的子图
    for j in range(min(6, len(imgs))*2, 12):
        row = j // 4
        axes[row, j%4].axis('off')

    fig.suptitle('多图颜色直方图对比', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_多图颜色直方图.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'images_compared': min(6, len(imgs))})
