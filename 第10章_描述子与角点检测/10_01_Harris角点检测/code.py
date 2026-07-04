#!/usr/bin/env python3
"""真实执行源码 — 10_01_Harris角点检测"""
def exp_10_1():
    """实验1: Harris角点检测"""
    eid = '10_01_Harris角点检测'
    d = exp_start(eid, 'Harris角点检测')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_f = np.float32(gray)

    # Harris角点
    dst = cv2.cornerHarris(gray_f, 2, 3, 0.04)
    dst_dilated = cv2.dilate(dst, None)

    harris_img = img.copy()
    harris_img[dst > 0.01 * dst.max()] = [255, 0, 0]

    # 图1: Harris过程
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(img); axes[0].set_title('原图', fontproperties=FONT); axes[0].axis('off')
    axes[1].imshow(dst, cmap='hot'); axes[1].set_title('Harris响应图', fontproperties=FONT); axes[1].axis('off')
    axes[2].imshow(harris_img); axes[2].set_title('Harris角点 (阈值=0.01×max)', fontproperties=FONT); axes[2].axis('off')
    fig.suptitle('Harris角点检测', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_Harris角点.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 不同k值
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    k_values = [0.01, 0.04, 0.06, 0.08, 0.10, 0.15]
    for i, k in enumerate(k_values):
        ax = axes[i//3, i%3]
        dst_k = cv2.cornerHarris(gray_f, 2, 3, k)
        img_k = img.copy()
        img_k[dst_k > 0.01 * dst_k.max()] = [255, 0, 0]
        ax.imshow(img_k)
        n_corners = np.sum(dst_k > 0.01 * dst_k.max())
        ax.set_title(f'k={k} ({n_corners}角点)', fontproperties=FONT, fontsize=9)
        ax.axis('off')
    fig.suptitle('Harris参数k值对比', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_Harris_k值对比.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'corners_found': int(np.sum(dst > 0.01 * dst.max()))})
