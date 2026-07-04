#!/usr/bin/env python3
"""真实执行源码 — 05_02_图像灰度化"""
def exp_5_2(img=None):
    """实验2: 图像灰度化 - 多种灰度化方法对比"""
    eid = '05_02_图像灰度化'
    d = exp_start(eid, '图像灰度化')
    files = []

    if img is None:
        img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))

    # 三种灰度化方法
    gray_avg = np.mean(img, axis=2).astype(np.uint8)  # 平均值法
    gray_w = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)     # 加权法 (cv2)
    # 自定义加权
    gray_custom = (0.299 * img[:,:,0] + 0.587 * img[:,:,1] + 0.114 * img[:,:,2]).astype(np.uint8)

    methods = [
        (img, '原图(RGB)'),
        (gray_avg, '平均值法\n(R+G+B)/3'),
        (gray_w, 'OpenCV加权法\n0.299R+0.587G+0.114B'),
        (gray_custom, '自定义加权\n同公式'),
    ]

    fig = make_montage([m[0] for m in methods], [m[1] for m in methods], cols=4, figsize=(16, 4),
                       main_title='图像灰度化 — 三种方法对比')
    p1 = os.path.join(d, '01_灰度化方法对比.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 灰度直方图对比
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for ax, (gray, name) in zip(axes, [('avg', gray_avg), ('cv2', gray_w), ('custom', gray_custom)]):
        ax.hist(gray.ravel(), bins=256, range=(0, 255), color='gray', alpha=0.7)
        ax.set_title(f'{name}灰度直方图', fontproperties=FONT)
        ax.set_xlim(0, 255)
    fig.suptitle('灰度直方图对比', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_灰度直方图对比.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'methods': 3})
    return gray_w
