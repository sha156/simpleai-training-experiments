#!/usr/bin/env python3
"""真实执行源码 — 17_04_KMeans图像分割"""
def exp_17_4():
    """实验4: K-Means图像分割"""
    eid = '17_04_KMeans图像分割'
    d = exp_start(eid, 'KMeans图像分割')
    files = []

    import cv2
    img = cv2.imread(os.path.join(DATA_CV, 'lena.jpg'))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img_rgb.reshape(-1, 3).astype(np.float32)

    results_km = []
    for k in [2, 3, 4, 6, 8, 12]:
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        segmented = centers[labels.flatten()].reshape(img_rgb.shape)
        results_km.append((segmented, f'K={k}'))

    # 图1: 不同K值分割
    fig = make_montage(
        [img_rgb] + [r[0] for r in results_km],
        ['原图'] + [r[1] for r in results_km],
        cols=4, figsize=(18, 10),
        main_title='K-Means颜色量化分割'
    )
    p1 = os.path.join(d, '01_KMeans分割.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 颜色调色板
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    for i, (k, (_, _, centers)) in enumerate(zip([2,3,4,6,8,12], [
        (2, None, cv2.kmeans(pixels, 2, None, (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0), 10, cv2.KMEANS_RANDOM_CENTERS)[2]),
        (3, None, cv2.kmeans(pixels, 3, None, (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0), 10, cv2.KMEANS_RANDOM_CENTERS)[2]),
        None, None, None, None
    ])):
        ax = axes[i//3, i%3]
        # 直接重新算每个K
        _, _, c = cv2.kmeans(pixels, k, None, (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0), 10, cv2.KMEANS_RANDOM_CENTERS)
        palette = np.uint8(c).reshape(1, k, 3)
        ax.imshow(palette, aspect='auto')
        ax.set_title(f'K={k} 调色板', fontproperties=FONT)
        ax.axis('off')

    fig.suptitle('K-Means颜色调色板', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_KMeans调色板.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'k_values': [2,3,4,6,8,12]})
