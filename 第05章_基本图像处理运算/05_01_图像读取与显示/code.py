#!/usr/bin/env python3
"""真实执行源码 — 05_01_图像读取与显示"""
def exp_5_1():
    """实验1: 图像读取与显示 - 读取多种格式图片，展示基本信息"""
    eid = '05_01_图像读取与显示'
    d = exp_start(eid, '图像读取与显示')
    files = []

    paths = [
        os.path.join(DATA_CV, 'lena.jpg'),
        os.path.join(DATA_CV, 'Lincoln.png'),
        os.path.join(DATA_CV, 'fruit.png'),
        os.path.join(DATA_CV, 'house.jpg'),
    ]

    imgs, infos = [], []
    for p in paths:
        if not os.path.exists(p): continue
        img_cv = cv2.imread(p)
        if img_cv is None: continue
        h, w, c = img_cv.shape if img_cv.ndim == 3 else (*img_cv.shape, 1)
        sz = os.path.getsize(p)
        imgs.append(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB) if c == 3 else img_cv)
        infos.append(f'{os.path.basename(p)}\n{w}×{h}×{c}ch\n{sz/1024:.0f}KB')

    # 图1: 四图拼接展示
    fig = make_montage(imgs, infos, cols=2, figsize=(12, 10), main_title='图像读取与显示 — 多种格式')
    p1 = os.path.join(d, '01_多格式图像展示.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 单图详细信息展示
    img = imgs[0]
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    axes[0].imshow(img); axes[0].set_title('原图(RGB)', fontproperties=FONT)
    # R通道
    axes[1].imshow(img[:,:,0], cmap='Reds'); axes[1].set_title('R通道', fontproperties=FONT)
    # G通道
    axes[2].imshow(img[:,:,1], cmap='Greens'); axes[2].set_title('G通道', fontproperties=FONT)
    fig.suptitle('图像通道分解', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_通道分解.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'images_loaded': len(imgs)})
    return imgs[0] if imgs else None
