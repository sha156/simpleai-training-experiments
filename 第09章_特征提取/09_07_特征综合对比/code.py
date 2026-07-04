#!/usr/bin/env python3
"""真实执行源码 — 09_07_特征综合对比"""
def exp_9_7():
    """实验7: 特征可视化综合对比 (SIFT vs HOG vs LBP vs Color)"""
    eid = '09_07_特征综合对比'
    d = exp_start(eid, '特征综合对比')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # SIFT
    sift = cv2.xfeatures2d.SIFT_create()
    kp = sift.detect(gray, None)
    sift_img = cv2.drawKeypoints(img, kp, None, color=(0, 255, 0))

    # HOG visualization
    small = cv2.resize(gray, (64, 128))
    try:
        from skimage.feature import hog
        _, hog_img = hog(small, orientations=9, pixels_per_cell=(8, 8),
                        cells_per_block=(2, 2), visualize=True)
        hog_display = cv2.resize(hog_img, gray.shape[::-1])
    except:
        hog_display = np.zeros_like(gray)

    # Canny edges
    canny_img = cv2.Canny(gray, 50, 150)

    # Color histogram
    color_hist_img = np.zeros((256, 256*3, 3), dtype=np.uint8)
    for i, color in enumerate([(255,0,0), (0,255,0), (0,0,255)]):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
        for j in range(1, 256):
            cv2.line(color_hist_img, (j-1 + i*256, 255 - int(hist[j-1])),
                    (j + i*256, 255 - int(hist[j])), color, 1)

    # 汇总图
    fig = make_montage(
        [img, sift_img, hog_display, canny_img],
        ['原图', f'SIFT ({len(kp)}个关键点)', 'HOG梯度直方图', 'Canny边缘'],
        cols=2, figsize=(14, 12),
        main_title='多特征提取综合对比'
    )
    p1 = os.path.join(d, '01_特征综合对比.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'features': ['SIFT','HOG','Canny','ColorHist']})


# ══════════════════════════════════════════════════════════════
#  第10章: 描述子与角点检测 (4个实验)
# ══════════════════════════════════════════════════════════════
