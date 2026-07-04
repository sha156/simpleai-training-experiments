#!/usr/bin/env python3
"""真实执行源码 — 08_02_OpenCV鼠标交互"""
def exp_8_2():
    """实验2: OpenCV鼠标事件与交互"""
    eid = '08_02_OpenCV鼠标交互'
    d = exp_start(eid, 'OpenCV鼠标交互')
    files = []

    # 用matplotlib模拟交互演示
    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    h, w = img.shape[:2]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    # 模拟鼠标画矩形ROI
    roi_img = img.copy()
    cv2.rectangle(roi_img, (80, 80), (280, 280), (255, 0, 0), 3)
    roi_img[80:280, 80:280] = roi_img[80:280, 80:280] * 0.8 + np.array([50, 50, 200]) * 0.2
    axes[0].imshow(img); axes[0].set_title('原图', fontproperties=FONT); axes[0].axis('off')
    axes[1].imshow(roi_img); axes[1].set_title('鼠标框选ROI', fontproperties=FONT); axes[1].axis('off')

    # 模拟画多边形
    poly_img = img.copy()
    pts = np.array([[100,100],[180,60],[280,100],[300,200],[250,280],[150,260],[80,200]], np.int32)
    cv2.polylines(poly_img, [pts], True, (0, 255, 0), 3)
    cv2.fillPoly(poly_img, [pts], (0, 255, 0, 64))
    axes[2].imshow(poly_img); axes[2].set_title('鼠标绘制多边形', fontproperties=FONT); axes[2].axis('off')

    fig.suptitle('OpenCV鼠标交互演示', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_鼠标交互演示.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})
