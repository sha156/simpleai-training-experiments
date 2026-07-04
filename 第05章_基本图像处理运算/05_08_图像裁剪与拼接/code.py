#!/usr/bin/env python3
"""真实执行源码 — 05_08_图像裁剪与拼接"""
def exp_5_8():
    """实验8: 图像裁剪、拼接与融合"""
    eid = '05_08_图像裁剪与拼接'
    d = exp_start(eid, '图像裁剪与拼接')
    files = []

    imgs, names = get_real_images(4)

    # 图1: 裁剪演示
    img = imgs[0]
    h, w = img.shape[:2]
    crops = [
        img[0:h//2, 0:w//2],        # 左上
        img[0:h//2, w//2:w],         # 右上
        img[h//2:h, 0:w//2],         # 左下
        img[h//2:h, w//2:w],         # 右下
        img[h//4:3*h//4, w//4:3*w//4], # 中心
    ]
    fig = make_montage(
        [img] + crops,
        ['原图', '左上1/4', '右上1/4', '左下1/4', '右下1/4', '中心1/2'],
        cols=3, figsize=(14, 9),
        main_title='图像区域裁剪'
    )
    p1 = os.path.join(d, '01_区域裁剪.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 拼接 - 水平+垂直拼接
    if len(imgs) >= 4:
        imgs_resized = [cv2.resize(im, (200, 200)) for im in imgs[:4]]
        hstack = np.hstack(imgs_resized[:2])
        vstack = np.vstack(imgs_resized[2:])
        combined = np.vstack([hstack, vstack])

        fig, ax = plt.subplots(figsize=(12, 10))
        ax.imshow(combined)
        ax.set_title('四图拼接 (2×2网格)', fontproperties=FONT, fontsize=14)
        ax.axis('off')
        fig.tight_layout()
        p2 = os.path.join(d, '02_图像拼接.png')
        save_img(fig, p2); files.append(p2)

    # 图3: 图像融合 (alpha blending)
    if len(imgs) >= 2:
        im1 = cv2.resize(imgs[0], (256, 256))
        im2 = cv2.resize(imgs[1], (256, 256))
        alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
        blends = [cv2.addWeighted(im1, a, im2, 1-a, 0) for a in alphas]
        fig = make_montage(
            blends,
            [f'α={a:.2f}' for a in alphas],
            cols=5, figsize=(18, 4),
            main_title='图像融合 (Alpha Blending)'
        )
        p3 = os.path.join(d, '03_图像融合.png')
        save_img(fig, p3); files.append(p3)

    exp_done(eid, d, files, {'crops': 5})
