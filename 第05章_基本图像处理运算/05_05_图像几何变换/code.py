#!/usr/bin/env python3
"""真实执行源码 — 05_05_图像几何变换"""
def exp_5_5():
    """实验5: 图像几何变换 - 平移、旋转、缩放、仿射"""
    eid = '05_05_图像几何变换'
    d = exp_start(eid, '图像几何变换')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    if img is None: img = load_rgb(os.path.join(DATA_CV, 'house.jpg'))
    h, w = img.shape[:2]

    # 平移
    M_trans = np.float32([[1, 0, 50], [0, 1, 30]])
    trans = cv2.warpAffine(img, M_trans, (w, h))

    # 旋转
    M_rot = cv2.getRotationMatrix2D((w/2, h/2), 30, 1.0)
    rot = cv2.warpAffine(img, M_rot, (w, h))

    # 仿射
    pts1 = np.float32([[50,50],[200,50],[50,200]])
    pts2 = np.float32([[10,100],[200,50],[100,250]])
    M_aff = cv2.getAffineTransform(pts1, pts2)
    aff = cv2.warpAffine(img, M_aff, (w, h))

    # 透视
    pts1_p = np.float32([[0,0],[w-1,0],[0,h-1],[w-1,h-1]])
    pts2_p = np.float32([[30,20],[w-50,10],[20,h-40],[w-30,h-20]])
    M_persp = cv2.getPerspectiveTransform(pts1_p, pts2_p)
    persp = cv2.warpPerspective(img, M_persp, (w, h))

    fig = make_montage(
        [img, trans, rot, aff, persp],
        ['原图', '平移 (50,30)', '旋转 30°', '仿射变换', '透视变换'],
        cols=3, figsize=(16, 10),
        main_title='图像几何变换'
    )
    p1 = os.path.join(d, '01_几何变换汇总.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 旋转角度序列
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    for i, ang in enumerate(angles):
        ax = axes[i//4, i%4]
        M = cv2.getRotationMatrix2D((w/2, h/2), ang, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h))
        ax.imshow(rotated)
        ax.set_title(f'{ang}°', fontproperties=FONT)
        ax.axis('off')
    fig.suptitle('多角度旋转', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_多角度旋转.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'transforms': ['translate','rotate','affine','perspective']})
