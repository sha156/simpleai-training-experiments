#!/usr/bin/env python3
"""真实执行源码 — 05_07_图像旋转与翻转"""
def exp_5_7():
    """实验7: 图像旋转与翻转"""
    eid = '05_07_图像旋转与翻转'
    d = exp_start(eid, '图像旋转与翻转')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    if img is None: img = load_rgb(os.path.join(DATA_CV, 'house.jpg'))

    # 各种翻转
    flip_h = cv2.flip(img, 1)
    flip_v = cv2.flip(img, 0)
    flip_both = cv2.flip(img, -1)

    # 各种旋转
    h, w = img.shape[:2]
    M90 = cv2.getRotationMatrix2D((w/2, h/2), 90, 1.0)
    rot90 = cv2.warpAffine(img, M90, (w, h))

    # 转置
    transp = cv2.transpose(img)

    fig = make_montage(
        [img, flip_h, flip_v, flip_both, rot90, transp],
        ['原图', '水平翻转', '垂直翻转', '水平+垂直', '旋转90°', '转置'],
        cols=3, figsize=(15, 10),
        main_title='图像旋转与翻转'
    )
    p1 = os.path.join(d, '01_旋转与翻转.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'operations': ['flip_h','flip_v','flip_both','rotate90','transpose']})
