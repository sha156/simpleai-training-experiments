#!/usr/bin/env python3
"""真实执行源码 — 06_01_空间域滤波"""
def exp_6_1():
    """实验1: 空间域滤波 - 平滑、锐化、边缘检测"""
    eid = '06_01_空间域滤波'
    d = exp_start(eid, '空间域滤波')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 各种空间域滤波
    # 平滑
    blur_mean = cv2.blur(img, (5, 5))
    blur_gauss = cv2.GaussianBlur(img, (5, 5), 0)
    blur_median = cv2.medianBlur(img, 5)
    blur_bilateral = cv2.bilateralFilter(img, 9, 75, 75)

    # 锐化
    kernel_sharpen = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]) / 1
    sharpen = cv2.filter2D(img, -1, kernel_sharpen)

    # 边缘
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel_abs = np.sqrt(sobel_x**2 + sobel_y**2)
    sobel_abs = np.clip(sobel_abs, 0, 255).astype(np.uint8)

    # 图1: 平滑滤波汇总
    fig = make_montage(
        [img, blur_mean, blur_gauss, blur_median, blur_bilateral, sharpen],
        ['原图', '均值滤波 5×5', '高斯滤波 5×5', '中值滤波 5', '双边滤波', '锐化'],
        cols=3, figsize=(16, 10),
        main_title='空间域滤波 — 平滑与锐化'
    )
    p1 = os.path.join(d, '01_平滑与锐化.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 梯度检测
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    for ax, (data, name) in zip(axes, [
        (gray, '原图(灰度)'),
        (np.abs(sobel_x).astype(np.uint8), 'Sobel X梯度'),
        (np.abs(sobel_y).astype(np.uint8), 'Sobel Y梯度'),
        (sobel_abs, '梯度幅值')
    ]):
        ax.imshow(data, cmap='gray')
        ax.set_title(name, fontproperties=FONT)
        ax.axis('off')
    fig.suptitle('空间域梯度检测 (Sobel算子)', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_Sobel梯度.png')
    save_img(fig, p2); files.append(p2)

    # 图3: 不同核大小的高斯模糊
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    for i, k in enumerate([3, 5, 7, 9, 15, 31]):
        ax = axes[i//3, i%3]
        blurred = cv2.GaussianBlur(img, (k, k), 0)
        ax.imshow(blurred)
        ax.set_title(f'高斯核 {k}×{k}', fontproperties=FONT)
        ax.axis('off')
    fig.suptitle('高斯滤波核大小对比', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p3 = os.path.join(d, '03_高斯核大小对比.png')
    save_img(fig, p3); files.append(p3)

    exp_done(eid, d, files, {'filters': ['mean','gaussian','median','bilateral','sharpen','sobel']})
