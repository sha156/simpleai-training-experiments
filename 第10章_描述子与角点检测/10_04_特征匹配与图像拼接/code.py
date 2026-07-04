#!/usr/bin/env python3
"""真实执行源码 — 10_04_特征匹配与图像拼接"""
def exp_10_4():
    """实验4: 特征匹配与拼接"""
    eid = '10_04_特征匹配与图像拼接'
    d = exp_start(eid, '特征匹配与图像拼接')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))

    if img is not None:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        h, w = gray.shape

        # 模拟两张有重叠的图像
        left = gray[:, :w*3//4]
        right = gray[:, w//4:]
        left_rgb = img[:, :w*3//4].copy()
        right_rgb = img[:, w//4:].copy()

        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(left, None)
        kp2, des2 = sift.detectAndCompute(right, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        good = [m for m, n in matches if m.distance < 0.75 * n.distance]

        # 图1: 重叠区域匹配
        match_img = cv2.drawMatches(left_rgb, kp1, right_rgb, kp2, good, None,
                                     flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        axes[0].imshow(img); axes[0].set_title('完整原图', fontproperties=FONT); axes[0].axis('off')
        axes[1].imshow(match_img)
        axes[1].set_title(f'左右图像SIFT匹配 ({len(good)}对)', fontproperties=FONT); axes[1].axis('off')
        fig.suptitle('基于特征匹配的图像拼接演示', fontproperties=FONT, fontsize=14)
        fig.tight_layout()
        p1 = os.path.join(d, '01_拼接匹配.png')
        save_img(fig, p1); files.append(p1)

        # 图2: 单应性估计示意
        if len(good) >= 4:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M_h, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matches_mask = mask.ravel().tolist()

            inliers = sum(matches_mask)

            draw_params = dict(matchColor=(0, 255, 0), singlePointColor=None,
                              matchesMask=matches_mask, flags=2)
            ransac_img = cv2.drawMatches(left_rgb, kp1, right_rgb, kp2, good, None, **draw_params)

            fig, ax = plt.subplots(figsize=(16, 8))
            ax.imshow(ransac_img)
            ax.set_title(f'RANSAC筛选后匹配 ({inliers}内点/{len(good)}总匹配)', fontproperties=FONT, fontsize=14)
            ax.axis('off')
            fig.tight_layout()
            p2 = os.path.join(d, '02_RANSAC匹配.png')
            save_img(fig, p2); files.append(p2)

            exp_done(eid, d, files, {'matches': len(good), 'inliers': inliers})
        else:
            exp_done(eid, d, files, {'matches': len(good)})
    else:
        exp_done(eid, d, files, {})


# ══════════════════════════════════════════════════════════════
#  第13章: 三维视觉 (2个实验)
# ══════════════════════════════════════════════════════════════
