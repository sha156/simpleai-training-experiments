#!/usr/bin/env python3
"""真实执行源码 — 17_02_KNN图像分类"""
def fix_17_02():
    """KNN图像分类"""
    d = OUT_DIRS[5]
    files = []
    from sklearn.datasets import load_digits
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    digits = load_digits()
    X, y = digits.data, digits.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # K值测试
    k_values = [1, 3, 5, 7, 9, 11, 15, 21, 31]
    accs = [accuracy_score(y_test, KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train).predict(X_test)) for k in k_values]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(k_values, accs, 'b-o', markersize=8, linewidth=2)
    best_k = k_values[np.argmax(accs)]
    axes[0].axvline(best_k, color='r', linestyle='--', label=f'最优k={best_k}')
    axes[0].set_title('K值对KNN准确率的影响', fontproperties=FONT)
    axes[0].set_xlabel('K'); axes[0].set_ylabel('准确率')
    axes[0].legend(prop=FONT); axes[0].grid(True, alpha=0.3)

    # 邻居示例
    knn = KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)
    dists, neighbors = knn.kneighbors([X_test[0]], n_neighbors=3)
    axes[1].axis('off')
    axes[1].imshow(X_test[0].reshape(8,8), cmap='gray')
    pred = knn.predict([X_test[0]])[0]
    axes[1].set_title(f'测试样本 真实={y_test[0]} 预测={pred}', fontproperties=FONT, fontsize=10)

    fig.suptitle('KNN图像分类', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p = os.path.join(d, '01_KNN_k值分析.png')
    save_img(fig, p); files.append(p)

    # 邻居可视化
    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    axes[0].imshow(X_test[0].reshape(8,8), cmap='gray'); axes[0].set_title(f'测试\n真={y_test[0]}', fontproperties=FONT, fontsize=8); axes[0].axis('off')
    for i, n_idx in enumerate(neighbors[0]):
        axes[i+1].imshow(X_train[n_idx].reshape(8,8), cmap='gray')
        axes[i+1].set_title(f'邻居{i+1}\n={y_train[n_idx]}', fontproperties=FONT, fontsize=8); axes[i+1].axis('off')
    fig.suptitle(f'KNN最近邻示例 (k=3, 预测={pred})', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_最近邻示例.png')
    save_img(fig, p2); files.append(p2)

    with open(os.path.join(d, 'results.json'), 'w') as f:
        json.dump({'files': files, 'best_k': best_k, 'best_acc': float(max(accs))}, f)
    print(f'17_02: {len(files)} files OK')

# Run remaining fixes (first 2 already done)
for d in OUT_DIRS:
    os.makedirs(d, exist_ok=True)

fix_12_01()
fix_14_05()
fix_16_01()
fix_17_02()
print('Remaining 4 fixes done!')
