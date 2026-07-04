#!/usr/bin/env python3
"""真实执行源码 — 09_01_SIFT特征检测"""
def exp_9_1():
    """实验1: SIFT特征检测与可视化"""
    eid = '09_01_SIFT特征检测'
    d = exp_start(eid, 'SIFT特征检测')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # SIFT特征
    sift = cv2.xfeatures2d.SIFT_create()
    kp = sift.detect(gray, None)

    # 画特征点
    img_kp = cv2.drawKeypoints(img, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
                                color=(0, 255, 0))

    # 图1: SIFT全部特征点
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    axes[0].imshow(img); axes[0].set_title('原图', fontproperties=FONT); axes[0].axis('off')
    axes[1].imshow(img_kp); axes[1].set_title(f'SIFT特征点 ({len(kp)}个)', fontproperties=FONT); axes[1].axis('off')
    fig.suptitle('SIFT特征点检测', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_SIFT特征点.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 按响应强度排序的Top特征点
    kp_sorted = sorted(kp, key=lambda x: x.response, reverse=True)
    for top_n in [10, 25, 50, 100]:
        img_top = img.copy()
        for k in kp_sorted[:top_n]:
            cv2.circle(img_top, (int(k.pt[0]), int(k.pt[1])), int(k.size//2), (0, 255, 0), 2)

    fig, axes = plt.subplots(1, 4, figsize=(18, 4))
    for i, n in enumerate([10, 25, 50, 100]):
        img_top = img.copy()
        for k in kp_sorted[:n]:
            cv2.circle(img_top, (int(k.pt[0]), int(k.pt[1])), int(k.size//2+1), (0, 255, 0), 1)
        axes[i].imshow(img_top)
        axes[i].set_title(f'Top {n} 特征点', fontproperties=FONT)
        axes[i].axis('off')
    fig.suptitle('SIFT特征点按响应强度排序', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_SIFT_Top特征点.png')
    save_img(fig, p2); files.append(p2)

    # 图3: 特征点尺度+方向分布
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    sizes = [k.size for k in kp]
    responses = [k.response for k in kp]
    angles = [k.angle for k in kp]

    axes[0].hist(sizes, bins=30, color='#2196F3', alpha=0.7)
    axes[0].set_title('特征点尺度分布', fontproperties=FONT)
    axes[0].set_xlabel('尺度', fontproperties=FONT)

    axes[1].hist(responses, bins=30, color='#4CAF50', alpha=0.7)
    axes[1].set_title('特征点响应强度分布', fontproperties=FONT)
    axes[1].set_xlabel('响应值', fontproperties=FONT)

    axes[2].hist(angles, bins=36, color='#FF9800', alpha=0.7)
    axes[2].set_title('特征点方向分布', fontproperties=FONT)
    axes[2].set_xlabel('角度(°)', fontproperties=FONT)

    fig.suptitle('SIFT特征点统计分析', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p3 = os.path.join(d, '03_SIFT统计分析.png')
    save_img(fig, p3); files.append(p3)

    exp_done(eid, d, files, {'keypoints': len(kp), 'avg_response': float(np.mean(responses))})
