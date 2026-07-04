#!/usr/bin/env python3
"""真实执行源码 — 10_03_SIFT描述子匹配"""
def exp_10_3():
    """实验3: SIFT描述子匹配"""
    eid = '10_03_SIFT描述子匹配'
    d = exp_start(eid, 'SIFT描述子匹配')
    files = []

    img1 = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    img2 = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))

    if img1 is not None:
        # 对同一图做变换得到第二张
        gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        # 旋转+缩放
        h, w = gray1.shape
        M = cv2.getRotationMatrix2D((w/2, h/2), 15, 0.9)
        gray2 = cv2.warpAffine(gray1, M, (w, h))
        img2 = cv2.warpAffine(img1, M, (w, h))

        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(gray1, None)
        kp2, des2 = sift.detectAndCompute(gray2, None)

        # BF匹配
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # Lowe's ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)

        match_img = cv2.drawMatches(img1, kp1, img2, kp2, good, None,
                                     flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        fig, axes = plt.subplots(1, 2, figsize=(18, 8))
        axes[0].imshow(img1); axes[0].set_title(f'图1 ({len(kp1)}个SIFT关键点)', fontproperties=FONT); axes[0].axis('off')
        axes[1].imshow(match_img)
        axes[1].set_title(f'SIFT匹配 ({len(good)}对, Lowe ratio<0.75)', fontproperties=FONT); axes[1].axis('off')
        fig.suptitle('SIFT描述子特征匹配', fontproperties=FONT, fontsize=14)
        fig.tight_layout()
        p1 = os.path.join(d, '01_SIFT匹配.png')
        save_img(fig, p1); files.append(p1)

        # 图2: 距离分布 + ratio分布
        all_distances = [m.distance for m, n in matches]
        ratios = [m.distance / (n.distance + 1e-10) for m, n in matches]

        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        axes[0].hist(all_distances, bins=50, color='#2196F3', alpha=0.7)
        axes[0].axvline(np.median(all_distances), color='red', linestyle='--', label=f'中位数={np.median(all_distances):.1f}')
        axes[0].set_title('匹配距离分布', fontproperties=FONT)
        axes[0].legend(prop=FONT)

        axes[1].hist(ratios, bins=50, color='#FF9800', alpha=0.7)
        axes[1].axvline(0.75, color='red', linestyle='--', label='Lowe阈值=0.75')
        axes[1].set_title('最近邻距离比分布', fontproperties=FONT)
        axes[1].legend(prop=FONT)

        fig.suptitle('SIFT匹配统计分析', fontproperties=FONT, fontsize=14)
        fig.tight_layout()
        p2 = os.path.join(d, '02_匹配统计分析.png')
        save_img(fig, p2); files.append(p2)

        exp_done(eid, d, files, {'keypoints1': len(kp1), 'keypoints2': len(kp2), 'good_matches': len(good)})
    else:
        exp_done(eid, d, files, {})
