#!/usr/bin/env python3
"""真实执行源码 — 17_06_ML图像处理综合"""
def exp_17_6():
    """实验6: 机器学习图像处理综合对比"""
    eid = '17_06_ML图像处理综合'
    d = exp_start(eid, 'ML图像处理综合')
    files = []

    from sklearn.datasets import load_digits
    from sklearn.model_selection import train_test_split
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.decomposition import PCA
    from sklearn.metrics import accuracy_score

    digits = load_digits()
    X, y = digits.data, digits.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 原始特征
    clfs = {
        'SVM': SVC(kernel='rbf', gamma='scale'),
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5),
        'LogisticReg': LogisticRegression(max_iter=500, multi_class='ovr'),
    }

    results_raw = {}
    for name, clf in clfs.items():
        clf.fit(X_train, y_train)
        results_raw[name] = accuracy_score(y_test, clf.predict(X_test))

    # PCA降维后
    pca = PCA(n_components=16)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)

    results_pca = {}
    for name, clf in clfs.items():
        clf.fit(X_train_pca, y_train)
        results_pca[name] = accuracy_score(y_test, clf.predict(X_test_pca))

    # 图: 综合对比
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(clfs))
    w = 0.35
    ax.bar(x - w/2, list(results_raw.values()), w, label='原始特征(64维)', color='#2196F3', alpha=0.8)
    ax.bar(x + w/2, list(results_pca.values()), w, label='PCA降维(16维)', color='#FF9800', alpha=0.8)
    for i, (name, raw, pca_acc) in enumerate(zip(clfs.keys(), results_raw.values(), results_pca.values())):
        ax.text(i - w/2, raw + 0.01, f'{raw:.3f}', ha='center', fontsize=9)
        ax.text(i + w/2, pca_acc + 0.01, f'{pca_acc:.3f}', ha='center', fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(list(clfs.keys()), fontproperties=FONT, fontsize=12)
    ax.set_title('机器学习图像分类综合对比 (Digits数据集)', fontproperties=FONT, fontsize=14)
    ax.set_ylabel('准确率', fontproperties=FONT)
    ax.legend(prop=FONT)
    ax.set_ylim(0, 1.1)
    fig.tight_layout()
    p1 = os.path.join(d, '01_ML综合对比.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'raw_features': results_raw, 'pca_features': results_pca})


# ══════════════════════════════════════════════════════════════
#  主程序
# ══════════════════════════════════════════════════════════════
