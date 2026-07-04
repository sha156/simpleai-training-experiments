#!/usr/bin/env python3
"""真实执行源码 — 17_01_SVM图像分类"""
def exp_17_1():
    """实验1: SVM图像分类"""
    eid = '17_01_SVM图像分类'
    d = exp_start(eid, 'SVM图像分类')
    files = []

    import cv2
    from sklearn.svm import SVC
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix
    from sklearn.decomposition import PCA

    # 用MNIST
    from sklearn.datasets import load_digits
    digits = load_digits()
    X, y = digits.data, digits.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # PCA降维
    pca = PCA(n_components=32)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)

    # SVM
    svm = SVC(kernel='rbf', gamma='scale')
    svm.fit(X_train_pca, y_train)
    y_pred = svm.predict(X_test_pca)
    acc = np.mean(y_pred == y_test)

    # 图1: 样本展示+PCA
    fig, axes = plt.subplots(2, 5, figsize=(14, 6))
    for i in range(10):
        ax = axes[i//5, i%5]
        idx = np.where(y == i)[0][0]
        ax.imshow(digits.images[idx], cmap='gray')
        ax.set_title(f'数字 {i}', fontproperties=FONT)
        ax.axis('off')
    fig.suptitle('Digits数据集样本 (8×8像素)', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_数据样本.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 混淆矩阵
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(cm, cmap='Blues')
    for i in range(10):
        for j in range(10):
            ax.text(j, i, cm[i, j], ha='center', va='center',
                    color='white' if cm[i, j] > cm.max()/2 else 'black')
    ax.set_xticks(range(10)); ax.set_yticks(range(10))
    ax.set_xlabel('预测', fontproperties=FONT); ax.set_ylabel('真实', fontproperties=FONT)
    ax.set_title(f'SVM分类混淆矩阵 (准确率={acc:.3f})', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_SVM混淆矩阵.png')
    save_img(fig, p2); files.append(p2)

    # 图3: PCA方差解释
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    cumsum = np.cumsum(pca.explained_variance_ratio_)
    axes[0].bar(range(1, 33), pca.explained_variance_ratio_[:32], color='#2196F3', alpha=0.7)
    axes[0].set_title('PCA各成分方差解释率', fontproperties=FONT)
    axes[0].set_xlabel('主成分')

    axes[1].plot(range(1, 33), cumsum[:32], 'b-o', markersize=3, linewidth=2)
    axes[1].axhline(0.9, color='r', linestyle='--', label='90%阈值')
    axes[1].set_title(f'累积方差解释 (32维={cumsum[31]:.1%})', fontproperties=FONT)
    axes[1].set_xlabel('主成分数'); axes[1].legend(prop=FONT)

    fig.suptitle('PCA降维分析', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p3 = os.path.join(d, '03_PCA降维.png')
    save_img(fig, p3); files.append(p3)

    exp_done(eid, d, files, {'svm_accuracy': float(acc), 'n_components': 32})
