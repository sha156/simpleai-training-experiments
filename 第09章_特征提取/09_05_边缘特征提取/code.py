#!/usr/bin/env python3
"""真实执行源码 — 09_05_边缘特征提取"""
def exp_9_5():
    """实验5: 边缘特征提取 (Canny/Sobel/Prewitt/Laplacian)"""
    eid = '09_05_边缘特征提取'
    d = exp_start(eid, '边缘特征提取')
    files = []

    gray = load_gray(os.path.join(DATA_CV, 'lena.jpg'))
    gray_f = np.float32(gray)

    # 各种边缘检测
    canny = cv2.Canny(gray, 50, 150)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel = np.sqrt(sobel_x**2 + sobel_y**2)
    sobel = np.clip(sobel, 0, 255).astype(np.uint8)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian = np.clip(np.abs(laplacian), 0, 255).astype(np.uint8)

    # Scharr
    scharr_x = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
    scharr_y = cv2.Scharr(gray, cv2.CV_64F, 0, 1)
    scharr = np.sqrt(scharr_x**2 + scharr_y**2)
    scharr = np.clip(scharr, 0, 255).astype(np.uint8)

    fig = make_montage(
        [gray, canny, sobel, laplacian, scharr],
        ['原图(灰度)', 'Canny', 'Sobel幅值', 'Laplacian', 'Scharr幅值'],
        cols=3, figsize=(14, 8),
        main_title='边缘特征提取方法对比'
    )
    p1 = os.path.join(d, '01_边缘检测方法对比.png')
    save_img(fig, p1); files.append(p1)

    # 图2: Sobel方向
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    sobel_x_abs = np.clip(np.abs(sobel_x), 0, 255).astype(np.uint8)
    sobel_y_abs = np.clip(np.abs(sobel_y), 0, 255).astype(np.uint8)
    titles = ['原图', 'Sobel X', 'Sobel Y', '梯度方向']
    imgs_list = [gray, sobel_x_abs, sobel_y_abs, np.arctan2(sobel_y, sobel_x)]
    for ax, im, t in zip(axes, imgs_list, titles):
        ax.imshow(im, cmap='gray' if t != '梯度方向' else 'hsv')
        ax.set_title(t, fontproperties=FONT)
        ax.axis('off')
    fig.suptitle('Sobel梯度方向分析', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_Sobel方向分析.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'edge_methods': ['Canny','Sobel','Laplacian','Scharr']})
