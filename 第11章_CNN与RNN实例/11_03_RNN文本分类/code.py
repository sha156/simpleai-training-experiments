#!/usr/bin/env python3
"""真实执行源码 — 11_03_RNN文本分类"""
def exp_11_3():
    eid = '11_03_RNN文本分类'
    d = exp_start(eid, 'RNN文本分类')
    files = []
    import tensorflow as tf
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.imdb.load_data(num_words=5000)
    x_train = tf.keras.preprocessing.sequence.pad_sequences(x_train[:2000], maxlen=200)
    x_test_s = tf.keras.preprocessing.sequence.pad_sequences(x_test[:500], maxlen=200)

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(5000, 64, input_length=200),
        tf.keras.layers.LSTM(64, dropout=0.2), tf.keras.layers.Dense(1, activation='sigmoid')
    ]); model.compile('adam','binary_crossentropy',['accuracy'])
    h = model.fit(x_train, y_train[:2000], validation_data=(x_test_s, y_test[:500]), epochs=10, batch_size=64, verbose=0)
    _, acc = model.evaluate(x_test_s, y_test[:500], verbose=0)

    preds = model.predict(x_test_s[:200], verbose=0).flatten()
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(h.history['accuracy'], 'b-', label='训练'); axes[0].plot(h.history['val_accuracy'], 'r-', label='验证')
    axes[0].set_title(f'准确率 (测试={acc:.3f})', fontproperties=FONT); axes[0].legend(prop=FONT); axes[0].grid(True, alpha=0.3)
    axes[1].hist(preds[y_test[:200]==0], bins=20, alpha=0.6, label='负面', color='#F44336')
    axes[1].hist(preds[y_test[:200]==1], bins=20, alpha=0.6, label='正面', color='#4CAF50')
    axes[1].set_title('预测概率分布', fontproperties=FONT); axes[1].legend(prop=FONT); axes[1].axvline(0.5, color='black', linestyle='--')
    fig.suptitle('LSTM情感分类 (IMDB)', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_LSTM情感分类.png'); save_img(fig, p1); files.append(p1)
    exp_done(eid, d, files, {'test_accuracy': float(acc)})
