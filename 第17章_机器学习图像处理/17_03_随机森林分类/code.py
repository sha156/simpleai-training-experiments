#!/usr/bin/env python3
"""真实执行源码 — 17_03_随机森林分类"""
def exp_17_3():
    """实验3: 随机森林图像分类"""
    eid = '17_03_随机森林分类'
    d = exp_start(eid, '随机森林分类')
    files = []

    from sklearn.datasets import load_digits
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    digits = load_digits()
    X, y = digits.data, digits.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 不同树数量
    n_trees = [1, 5, 10, 20, 50, 100, 200]
    accs_rf = []
    for n in n_trees:
        rf = RandomForestClassifier(n_estimators=n, random_state=42, n_jobs=-1)
        rf.fit(X_train, y_train)
        accs_rf.append(accuracy_score(y_test, rf.predict(X_test)))

    # 特征重要性
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    importances = rf.feature_importances_

    # 图1: 树数量分析
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(n_trees, accs_rf, 'g-o', markersize=8, linewidth=2)
    axes[0].set_title('随机森林树数量对准确率的影响', fontproperties=FONT)
    axes[0].set_xlabel('树数量'); axes[0].set_ylabel('准确率')
    axes[0].grid(True, alpha=0.3)

    # 特征重要性热力图
    imp_img = importances.reshape(8, 8)
    axes[1].imshow(imp_img, cmap='hot')
    axes[1].set_title('像素重要性热力图', fontproperties=FONT)
    for i in range(8):
        for j in range(8):
            axes[1].text(j, i, f'{imp_img[i,j]:.1f}', ha='center', va='center',
                        fontsize=6, color='white' if imp_img[i,j] > 0.01 else 'black')
    fig.suptitle('随机森林图像分类', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_随机森林分析.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 分类器对比
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.linear_model import LogisticRegression

    classifiers = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM(RBF)': SVC(kernel='rbf'),
        'KNN(k=5)': KNeighborsClassifier(n_neighbors=5),
        'LogisticReg': LogisticRegression(max_iter=500, multi_class='ovr'),
    }
    clf_accs = {}
    for name, clf in classifiers.items():
        clf.fit(X_train, y_train)
        clf_accs[name] = accuracy_score(y_test, clf.predict(X_test))

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0']
    for i, (name, acc) in enumerate(clf_accs.items()):
        ax.bar(i, acc, color=colors[i], alpha=0.8)
        ax.text(i, acc + 0.005, f'{acc:.3f}', ha='center', fontsize=12)
    ax.set_xticks(range(4)); ax.set_xticklabels(list(clf_accs.keys()), fontproperties=FONT)
    ax.set_title('图像分类器对比', fontproperties=FONT, fontsize=14)
    ax.set_ylabel('准确率')
    ax.set_ylim(0, 1)
    fig.tight_layout()
    p2 = os.path.join(d, '02_分类器对比.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'classifiers': clf_accs})
