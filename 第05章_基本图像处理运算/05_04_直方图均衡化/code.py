#!/usr/bin/env python3
"""真实执行源码 — 05_04_直方图均衡化"""
def exp_5_4(gray=None):
    """实验4: 直方图均衡化"""
    eid = '05_04_直方图均衡化'
    d = exp_start(eid, '直方图均衡化')
    files = []

    # 用一张偏暗/偏亮的图演示效果更好
    imgs, names = get_real_images(3)
    if gray is None:
        dark_img = imgs[1] if len(imgs) > 1 else imgs[0]
        gray = cv2.cvtColor(dark_img, cv2.COLOR_RGB2GRAY) if dark_img.ndim == 3 else dark_img

    # CLAHE vs 普通均衡化
    equ = cv2.equalizeHist(gray)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahe_img = clahe.apply(gray)

    # 图1: 原图+普通均衡化+CLAHE
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    titles_row1 = ['原图', '普通均衡化', 'CLAHE自适应均衡化']
    imgs_row1 = [gray, equ, clahe_img]
    for i in range(3):
        axes[0, i].imshow(imgs_row1[i], cmap='gray')
        axes[0, i].set_title(titles_row1[i], fontproperties=FONT)
        axes[0, i].axis('off')
    for i in range(3):
        axes[1, i].hist(imgs_row1[i].ravel(), bins=256, range=(0,255), color='#555', alpha=0.8)
        axes[1, i].set_xlim(0, 255)
    fig.suptitle('直方图均衡化对比', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_均衡化对比.png')
    save_img(fig, p1); files.append(p1)

    # 图2: CLAHE不同参数
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    clips = [0.5, 1.0, 2.0, 3.0, 5.0, 10.0]
    for i, clip in enumerate(clips):
        ax = axes[i//3, i%3]
        c = cv2.createCLAHE(clipLimit=clip, tileGridSize=(8,8))
        ax.imshow(c.apply(gray), cmap='gray')
        ax.set_title(f'CLAHE clipLimit={clip}', fontproperties=FONT, fontsize=9)
        ax.axis('off')
    fig.suptitle('CLAHE参数对比', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_CLAHE参数对比.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'method': 'CLAHE+EqualizeHist'})
