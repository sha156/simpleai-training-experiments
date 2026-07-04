#!/usr/bin/env python3
"""真实执行源码 — 11_01_CNN图像分类"""
def exp_11_1():
    eid = '11_01_CNN图像分类'
    d = exp_start(eid, 'CNN图像分类')
    files = []
    import tensorflow as tf
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train = x_train[:3000].reshape(-1,28,28,1).astype('float32')/255.0
    x_test_s = x_test[:1000].reshape(-1,28,28,1).astype('float32')/255.0
    y_train_c = tf.keras.utils.to_categorical(y_train[:3000], 10)
    y_test_c = tf.keras.utils.to_categorical(y_test[:1000], 10)

    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32,3,activation='relu',input_shape=(28,28,1)),
        tf.keras.layers.MaxPooling2D(2), tf.keras.layers.Conv2D(64,3,activation='relu'),
        tf.keras.layers.MaxPooling2D(2), tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128,activation='relu'), tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(10,activation='softmax')
    ])
    model.compile('adam','categorical_crossentropy',['accuracy'])
    h = model.fit(x_train, y_train_c, validation_data=(x_test_s, y_test_c), epochs=12, batch_size=64, verbose=0)
    _, acc = model.evaluate(x_test_s, y_test_c, verbose=0)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(h.history['loss'], 'b-', label='训练'); axes[0].plot(h.history['val_loss'], 'r-', label='验证')
    axes[0].set_title('损失曲线', fontproperties=FONT); axes[0].legend(prop=FONT); axes[0].grid(True, alpha=0.3)
    axes[1].plot(h.history['accuracy'], 'b-', label='训练'); axes[1].plot(h.history['val_accuracy'], 'r-', label='验证')
    axes[1].set_title(f'准确率 (测试={acc:.3f})', fontproperties=FONT); axes[1].legend(prop=FONT); axes[1].grid(True, alpha=0.3)
    fig.suptitle('CNN MNIST分类', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_CNN训练曲线.png'); save_img(fig, p1); files.append(p1)

    # Predictions grid
    preds = model.predict(x_test_s[:25], verbose=0)
    pl, tl = np.argmax(preds, axis=1), np.argmax(y_test_c[:25], axis=1)
    fig, axes = plt.subplots(5, 5, figsize=(10, 10))
    for i, ax in enumerate(axes.flatten()):
        ax.imshow(x_test_s[i].reshape(28,28), cmap='gray')
        ax.set_title(f'T:{tl[i]} P:{pl[i]}', color='green' if pl[i]==tl[i] else 'red', fontproperties=FONT, fontsize=8)
        ax.axis('off')
    fig.suptitle('CNN预测结果', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_预测结果.png'); save_img(fig, p2); files.append(p2)

    from sklearn.metrics import confusion_matrix
    ap = np.argmax(model.predict(x_test_s, verbose=0), axis=1)
    cm = confusion_matrix(np.argmax(y_test_c, axis=1), ap)
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(cm, cmap='Blues')
    for i in range(10):
        for j in range(10):
            ax.text(j, i, cm[i,j], ha='center', va='center', color='white' if cm[i,j]>cm.max()/2 else 'black')
    ax.set_xticks(range(10)); ax.set_yticks(range(10))
    ax.set_xlabel('预测', fontproperties=FONT); ax.set_ylabel('真实', fontproperties=FONT)
    ax.set_title('混淆矩阵', fontproperties=FONT, fontsize=14)
    p3 = os.path.join(d, '03_混淆矩阵.png'); save_img(fig, p3); files.append(p3)
    exp_done(eid, d, files, {'accuracy': float(acc)})
