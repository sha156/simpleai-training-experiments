#!/usr/bin/env python3
"""真实执行源码 — 17_05_PCA图像压缩"""
def exp_17_5():
    """实验5: PCA图像压缩与重建"""
    eid = '17_05_PCA图像压缩'
    d = exp_start(eid, 'PCA图像压缩')
    files = []

    import cv2
    from sklearn.decomposition import PCA

    img = cv2.imread(os.path.join(DATA_CV, 'lena.jpg'), 0)
    if img is None:
        img = np.random.randint(0, 255, (128, 128), dtype=np.uint8)
    img_small = cv2.resize(img, (64, 64)).astype(np.float64) / 255.0

    # PCA压缩
    components_list = [1, 2, 4, 8, 16, 32, 48, 64]
    reconstructions = []

    for n_comp in components_list:
        pca = PCA(n_components=min(n_comp, img_small.shape[0]))
        transformed = pca.fit_transform(img_small)
        reconstructed = pca.inverse_transform(transformed)
        reconstructed = np.clip(reconstructed, 0, 1)
        reconstructions.append((reconstructed, f'PC={n_comp}'))

        mse = np.mean((img_small - reconstructed)**2)
        log_print('17.5', f'PC={n_comp}: MSE={mse:.6f}')

    # 图1
    fig = make_montage(
        [img_small] + [r[0] for r in reconstructions],
        ['原图(64×64)'] + [r[1] for r in reconstructions],
        cols=3, figsize=(16, 16),
        main_title='PCA图像压缩与重建'
    )
    p1 = os.path.join(d, '01_PCA压缩重建.png')
    save_img(fig, p1); files.append(p1)

    # 图2: MSE曲线
    mses = [np.mean((img_small - r[0])**2) for r in reconstructions]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(components_list, mses, 'b-o', markersize=8, linewidth=2)
    ax.set_xlabel('主成分数', fontproperties=FONT)
    ax.set_ylabel('MSE', fontproperties=FONT)
    ax.set_title('PCA压缩误差 vs 主成分数', fontproperties=FONT, fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    fig.tight_layout()
    p2 = os.path.join(d, '02_PCA误差曲线.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'components': components_list, 'mses': [float(m) for m in mses]})
