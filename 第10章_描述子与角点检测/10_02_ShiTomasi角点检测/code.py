#!/usr/bin/env python3
"""真实执行源码 — 10_02_ShiTomasi角点检测"""
def exp_10_2():
    """实验2: Shi-Tomasi角点检测"""
    eid = '10_02_ShiTomasi角点检测'
    d = exp_start(eid, 'Shi-Tomasi角点检测')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Shi-Tomasi
    corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
    corners = np.int0(corners)

    st_img = img.copy()
    for c in corners:
        x, y = c.ravel()
        cv2.circle(st_img, (x, y), 4, (0, 255, 0), -1)

    # 图1: Shi-Tomasi vs Harris
    gray_f = np.float32(gray)
    harris_dst = cv2.cornerHarris(gray_f, 2, 3, 0.04)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(st_img); axes[0].set_title(f'Shi-Tomasi角点 ({len(corners)}个)', fontproperties=FONT); axes[0].axis('off')

    harris_img = img.copy()
    harris_thresh = harris_dst > 0.01 * harris_dst.max()
    harris_img[harris_thresh] = [255, 0, 0]
    axes[1].imshow(harris_img)
    axes[1].set_title(f'Harris角点 ({np.sum(harris_thresh)}个)', fontproperties=FONT); axes[1].axis('off')

    fig.suptitle('Shi-Tomasi vs Harris角点检测对比', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_ShiTomasi_vs_Harris.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 不同质量等级
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    for i, quality in enumerate([0.001, 0.005, 0.01, 0.05, 0.1, 0.2]):
        ax = axes[i//3, i%3]
        try:
            corners_q = cv2.goodFeaturesToTrack(gray, 200, quality, 10)
            if corners_q is not None:
                img_q = img.copy()
                for c in np.int0(corners_q):
                    cv2.circle(img_q, tuple(c.ravel()), 4, (0, 255, 0), -1)
                ax.imshow(img_q)
                ax.set_title(f'quality={quality} ({len(corners_q)}个)', fontproperties=FONT, fontsize=9)
            else:
                ax.text(0.5, 0.5, '无角点', ha='center', transform=ax.transAxes)
        except:
            ax.text(0.5, 0.5, 'N/A', ha='center', transform=ax.transAxes)
        ax.axis('off')
    fig.suptitle('Shi-Tomasi质量等级参数对比', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_ShiTomasi质量等级.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'corners': len(corners)})
