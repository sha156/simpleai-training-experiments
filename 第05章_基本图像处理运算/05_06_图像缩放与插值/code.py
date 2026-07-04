#!/usr/bin/env python3
"""真实执行源码 — 05_06_图像缩放与插值"""
def exp_5_6():
    """实验6: 图像缩放与插值方法对比"""
    eid = '05_06_图像缩放与插值'
    d = exp_start(eid, '图像缩放与插值')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    h, w = img.shape[:2]
    nh, nw = h//4, w//4

    small = cv2.resize(img, (nw, nh))

    methods = {
        '最近邻': cv2.INTER_NEAREST,
        '双线性': cv2.INTER_LINEAR,
        '双三次': cv2.INTER_CUBIC,
        'Lanczos': cv2.INTER_LANCZOS4,
        '面积插值': cv2.INTER_AREA,
    }

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    for i, (name, method) in enumerate(methods.items()):
        upscaled = cv2.resize(small, (w, h), interpolation=method)
        axes[i].imshow(upscaled)
        axes[i].set_title(f'{name}放大×4', fontproperties=FONT)
        axes[i].axis('off')

    # 最后一个小窗展示原图
    axes[5].imshow(img)
    axes[5].set_title('原图(参考)', fontproperties=FONT)
    axes[5].axis('off')

    fig.suptitle('图像缩放 — 五种插值方法对比 (缩小4倍→放大4倍)', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_插值方法对比.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 局部放大对比
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    for i, (name, method) in enumerate(methods.items()):
        upscaled = cv2.resize(small, (w, h), interpolation=method)
        # 裁剪中心区域
        cy, cx = h//2, w//2
        crop = upscaled[cy-80:cy+80, cx-80:cx+80]
        axes[i//3, i%3].imshow(crop)
        axes[i//3, i%3].set_title(f'{name} (局部)', fontproperties=FONT)
        axes[i//3, i%3].axis('off')
    fig.suptitle('插值方法局部细节对比 (160×160)', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_插值局部细节.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'methods': list(methods.keys())})
