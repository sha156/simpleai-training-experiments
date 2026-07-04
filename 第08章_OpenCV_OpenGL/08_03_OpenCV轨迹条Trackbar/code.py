#!/usr/bin/env python3
"""真实执行源码 — 08_03_OpenCV轨迹条Trackbar"""
def exp_8_3():
    """实验3: OpenCV轨迹条Trackbar"""
    eid = '08_03_OpenCV轨迹条Trackbar'
    d = exp_start(eid, 'OpenCV轨迹条')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 模拟Trackbar效果: Canny不同阈值
    thresholds = [(30, 90), (50, 150), (80, 200), (100, 250), (150, 300)]

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    axes = axes.flatten()
    axes[0].imshow(gray, cmap='gray'); axes[0].set_title('原图(灰度)', fontproperties=FONT); axes[0].axis('off')

    for i, (low, high) in enumerate(thresholds):
        edges = cv2.Canny(gray, low, high)
        axes[i+1].imshow(edges, cmap='gray')
        axes[i+1].set_title(f'Canny({low}, {high})', fontproperties=FONT)
        axes[i+1].axis('off')

    fig.suptitle('Canny边缘检测 — Trackbar参数效果模拟', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_Canny参数对比.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 阈值Trackbar模拟
    thresholds_bin = [30, 60, 90, 120, 150, 180]
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    for i, th in enumerate(thresholds_bin):
        ax = axes[i//3, i%3]
        _, bw = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY)
        ax.imshow(bw, cmap='gray')
        ax.set_title(f'阈值={th}', fontproperties=FONT)
        ax.axis('off')
    fig.suptitle('二值化阈值Trackbar模拟', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_二值化Trackbar.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {})
