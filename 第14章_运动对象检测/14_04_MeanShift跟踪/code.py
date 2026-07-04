#!/usr/bin/env python3
"""真实执行源码 — 14_04_MeanShift跟踪"""
def exp_14_4():
    """实验4: MeanShift目标跟踪"""
    eid = '14_04_MeanShift跟踪'
    d = exp_start(eid, 'MeanShift跟踪')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # 选择ROI区域
    roi = hsv[80:200, 80:200]
    roi_hist = cv2.calcHist([roi], [0], None, [180], [0, 180])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    # 模拟跟踪
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    track_window = (80, 80, 120, 120)

    # 对原图做反投影
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

    # 图1: MeanShift过程
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(img); axes[0].set_title('原图', fontproperties=FONT); axes[0].axis('off')
    # 画初始ROI
    img_roi = img.copy()
    cv2.rectangle(img_roi, (80, 80), (200, 200), (0, 255, 0), 3)
    axes[1].imshow(img_roi); axes[1].set_title('初始ROI', fontproperties=FONT); axes[1].axis('off')
    axes[2].imshow(dst, cmap='hot'); axes[2].set_title('反向投影 (似然图)', fontproperties=FONT); axes[2].axis('off')
    fig.suptitle('MeanShift目标跟踪', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_MeanShift跟踪.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 不同迭代步骤
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    for i in range(6):
        ax = axes[i//3, i%3]
        shifted = img.copy()
        # 模拟窗口逐渐移动
        ox, oy = 80 + i*15, 80 + i*8
        cv2.rectangle(shifted, (ox, oy), (ox+120, oy+120), (0, 255, 0), 2)
        ax.imshow(shifted)
        ax.set_title(f'迭代{i+1}: ({ox},{oy})', fontproperties=FONT, fontsize=9)
        ax.axis('off')
    fig.suptitle('MeanShift跟踪迭代过程模拟', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_MeanShift迭代.png')
    save_img(fig, p2); files.append(p2)

    # 图3: ROI直方图
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(roi_hist, color='#4CAF50', linewidth=1)
    ax.set_title('目标ROI色调(H)直方图', fontproperties=FONT)
    ax.set_xlabel('色调(H) bin', fontproperties=FONT)
    ax.set_ylabel('频数', fontproperties=FONT)
    ax.set_xlim(0, 180)
    fig.tight_layout()
    p3 = os.path.join(d, '03_ROI直方图.png')
    save_img(fig, p3); files.append(p3)

    exp_done(eid, d, files, {})
