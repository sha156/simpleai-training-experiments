#!/usr/bin/env python3
"""真实执行源码 — 09_06_纹理特征GLCM"""
def exp_9_6():
    """实验6: 纹理特征提取 (GLCM灰度共生矩阵)"""
    eid = '09_06_纹理特征GLCM'
    d = exp_start(eid, '纹理特征GLCM')
    files = []

    gray = load_gray(os.path.join(DATA_CV, 'lena.jpg'))

    # 简单GLCM实现
    def glcm(img, d=1, theta=0, levels=256):
        h, w = img.shape
        glcm_matrix = np.zeros((levels, levels), dtype=np.float64)
        for i in range(h):
            for j in range(w):
                if theta == 0:  # 水平方向
                    j2 = j + d
                    if j2 < w:
                        glcm_matrix[img[i, j], img[i, j2]] += 1
                elif theta == 90:  # 垂直方向
                    i2 = i + d
                    if i2 < h:
                        glcm_matrix[img[i, j], img[i2, j]] += 1
        glcm_matrix = glcm_matrix / (glcm_matrix.sum() + 1e-10)
        return glcm_matrix

    # 降采样加速
    small = cv2.resize(gray, (64, 64))

    # 计算不同方向的GLCM
    glcm_0 = glcm(small, d=2, theta=0)
    glcm_90 = glcm(small, d=2, theta=90)

    # 图1: GLCM可视化 (只显示前64级)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    axes[0].imshow(small, cmap='gray'); axes[0].set_title('输入图像(64×64)', fontproperties=FONT); axes[0].axis('off')
    axes[1].imshow(glcm_0[:64,:64], cmap='hot'); axes[1].set_title('GLCM 水平方向 (d=2)', fontproperties=FONT)
    axes[2].imshow(glcm_90[:64,:64], cmap='hot'); axes[2].set_title('GLCM 垂直方向 (d=2)', fontproperties=FONT)
    fig.suptitle('灰度共生矩阵 (GLCM) 纹理分析', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_GLCM可视化.png')
    save_img(fig, p1); files.append(p1)

    # Haralick特征
    def haralick_features(g):
        contrast = np.sum((np.arange(g.shape[0])[:, None] - np.arange(g.shape[1]))**2 * g)
        homogeneity = np.sum(g / (1 + (np.arange(g.shape[0])[:, None] - np.arange(g.shape[1]))**2))
        energy = np.sum(g**2)
        entropy = -np.sum(g * np.log2(g + 1e-10))
        return {'对比度': contrast, '同质性': homogeneity, '能量': energy, '熵': entropy}

    features_0 = haralick_features(glcm_0)
    features_90 = haralick_features(glcm_90)

    # 图2: Haralick特征对比
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(features_0))
    w = 0.35
    ax.bar(x - w/2, list(features_0.values()), w, label='水平方向', color='#2196F3')
    ax.bar(x + w/2, list(features_90.values()), w, label='垂直方向', color='#FF9800')
    ax.set_xticks(x)
    ax.set_xticklabels(list(features_0.keys()), fontproperties=FONT)
    ax.set_title('Haralick纹理特征', fontproperties=FONT, fontsize=14)
    ax.legend(prop=FONT)
    fig.tight_layout()
    p2 = os.path.join(d, '02_Haralick特征.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, features_0)
