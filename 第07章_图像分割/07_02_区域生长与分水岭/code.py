#!/usr/bin/env python3
"""真实执行源码 — 07_02_区域生长与分水岭"""
def exp_7_2():
    """实验2: 区域生长与分水岭分割"""
    eid = '07_02_区域生长与分水岭'
    d = exp_start(eid, '区域生长与分水岭')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 分水岭算法
    # 1. 去噪+二值化
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 2. 形态学操作获取确定前景和背景
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.3 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # 3. 标记
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    # 4. 分水岭
    markers = cv2.watershed(img, markers)

    # 图1: 分水岭过程
    titles = ['原图', 'OTSU二值化', '距离变换', '确定前景', '分水岭标记', '分割结果']
    imgs_show = [img, binary, dist_transform/dist_transform.max(), sure_fg, markers, img.copy()]
    # 在结果图上画边界
    img_boundary = imgs_show[5].copy()
    img_boundary[markers == -1] = [255, 0, 0]

    fig = make_montage(
        [img, binary, dist_transform/dist_transform.max(), sure_fg,
         cv2.applyColorMap((markers*30 % 255).astype(np.uint8), cv2.COLORMAP_JET), img_boundary],
        ['原图', 'OTSU二值化', '距离变换', '确定前景', '标记区域', '分割边界(红色)'],
        cols=3, figsize=(16, 10),
        main_title='分水岭图像分割'
    )
    p1 = os.path.join(d, '01_分水岭分割.png')
    save_img(fig, p1); files.append(p1)

    # 图2: GrabCut
    mask = np.zeros(gray.shape, np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    rect = (30, 30, img.shape[1] - 60, img.shape[0] - 60)
    try:
        cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img_grab = img * mask2[:, :, np.newaxis]

        fig, axes = plt.subplots(1, 3, figsize=(14, 5))
        axes[0].imshow(img); axes[0].set_title('原图', fontproperties=FONT); axes[0].axis('off')
        axes[1].imshow(mask2, cmap='gray'); axes[1].set_title('GrabCut掩码', fontproperties=FONT); axes[1].axis('off')
        axes[2].imshow(img_grab); axes[2].set_title('GrabCut分割结果', fontproperties=FONT); axes[2].axis('off')
        fig.suptitle('GrabCut交互式分割', fontproperties=FONT, fontsize=14)
        fig.tight_layout()
        p2 = os.path.join(d, '02_GrabCut分割.png')
        save_img(fig, p2); files.append(p2)
    except:
        pass

    # 图3: 边缘检测用于分割 (Canny + 轮廓)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_img = img.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    axes[0].imshow(gray, cmap='gray'); axes[0].set_title('原图(灰度)', fontproperties=FONT); axes[0].axis('off')
    axes[1].imshow(edges, cmap='gray'); axes[1].set_title('Canny边缘检测', fontproperties=FONT); axes[1].axis('off')
    axes[2].imshow(contour_img); axes[2].set_title(f'轮廓检测 ({len(contours)}个轮廓)', fontproperties=FONT); axes[2].axis('off')
    fig.suptitle('基于边缘的图像分割', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p3 = os.path.join(d, '03_边缘轮廓分割.png')
    save_img(fig, p3); files.append(p3)

    exp_done(eid, d, files, {'methods': ['watershed','grabcut','canny_contour']})


# ══════════════════════════════════════════════════════════════
#  第8章: OpenCV/OpenGL (5个实验)
# ══════════════════════════════════════════════════════════════
