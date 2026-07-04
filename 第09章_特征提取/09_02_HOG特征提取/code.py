#!/usr/bin/env python3
"""真实执行源码 — 09_02_HOG特征提取"""
def exp_9_2():
    """实验2: HOG特征提取"""
    eid = '09_02_HOG特征提取'
    d = exp_start(eid, 'HOG特征提取')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'person.jpg'))
    if img is None: img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_resized = cv2.resize(gray, (64, 128))

    # HOG
    hog = cv2.HOGDescriptor()
    h = hog.compute(img_resized)

    # 可视化
    from skimage.feature import hog as skhog
    try:
        fd, hog_image = skhog(img_resized, orientations=9, pixels_per_cell=(8, 8),
                              cells_per_block=(2, 2), visualize=True)

        fig, axes = plt.subplots(1, 3, figsize=(14, 5))
        axes[0].imshow(img); axes[0].set_title('原图', fontproperties=FONT); axes[0].axis('off')
        axes[1].imshow(img_resized, cmap='gray'); axes[1].set_title('缩放至64×128', fontproperties=FONT); axes[1].axis('off')
        axes[2].imshow(hog_image, cmap='hot'); axes[2].set_title('HOG特征可视化', fontproperties=FONT); axes[2].axis('off')
        fig.suptitle('HOG (Histogram of Oriented Gradients) 特征', fontproperties=FONT, fontsize=14)
        fig.tight_layout()
        p1 = os.path.join(d, '01_HOG特征.png')
        save_img(fig, p1); files.append(p1)
    except:
        pass

    # 图2: 不同cell size对比
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    cell_sizes = [(4, 4), (8, 8), (16, 16)]
    for i, (cs, label) in enumerate([(4, '4×4'), (8, '8×8'), (16, '16×16')]):
        axes[0, i].set_title(f'cell={label}', fontproperties=FONT)
        try:
            _, hog_v = skhog(img_resized, orientations=9, pixels_per_cell=(cs, cs),
                           cells_per_block=(2, 2), visualize=True)
            axes[0, i].imshow(hog_v, cmap='hot')
        except:
            axes[0, i].text(0.5, 0.5, 'N/A', ha='center')
        axes[0, i].axis('off')

    for i, cs in enumerate([4, 8, 16]):
        axes[1, i].set_title(f'cell={cs}', fontproperties=FONT)
        try:
            fd, _ = skhog(img_resized, orientations=9, pixels_per_cell=(cs, cs),
                         cells_per_block=(2, 2), visualize=True)
            axes[1, i].bar(range(min(100, len(fd))), fd[:100])
        except:
            pass

    fig.suptitle('HOG参数对比', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_HOG参数对比.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'hog_descriptor_size': h.shape[0]})
