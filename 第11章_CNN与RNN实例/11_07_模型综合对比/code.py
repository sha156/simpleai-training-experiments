#!/usr/bin/env python3
"""真实执行源码 — 11_07_模型综合对比"""
def exp_11_7():
    eid = '11_07_模型综合对比'
    d = exp_start(eid, '模型综合对比')
    files = []
    import tensorflow as tf
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train = x_train[:2000].reshape(-1,28,28,1).astype('float32')/255.0
    x_test_s = x_test[:500].reshape(-1,28,28,1).astype('float32')/255.0
    y_train_c = tf.keras.utils.to_categorical(y_train[:2000], 10)
    y_test_c = tf.keras.utils.to_categorical(y_test[:500], 10)

    models = {
        'MLP': tf.keras.Sequential([tf.keras.layers.Flatten(input_shape=(28,28,1)), tf.keras.layers.Dense(128,activation='relu'), tf.keras.layers.Dense(64,activation='relu'), tf.keras.layers.Dense(10,activation='softmax')]),
        'CNN小': tf.keras.Sequential([tf.keras.layers.Conv2D(16,3,activation='relu',input_shape=(28,28,1)), tf.keras.layers.MaxPooling2D(2), tf.keras.layers.Flatten(), tf.keras.layers.Dense(10,activation='softmax')]),
        'CNN大': tf.keras.Sequential([tf.keras.layers.Conv2D(32,3,activation='relu',input_shape=(28,28,1)), tf.keras.layers.MaxPooling2D(2), tf.keras.layers.Conv2D(64,3,activation='relu'), tf.keras.layers.MaxPooling2D(2), tf.keras.layers.Flatten(), tf.keras.layers.Dense(128,activation='relu'), tf.keras.layers.Dropout(0.3), tf.keras.layers.Dense(10,activation='softmax')]),
    }
    results = {}
    for name, model in models.items():
        model.compile('adam','categorical_crossentropy',['accuracy'])
        h = model.fit(x_train, y_train_c, validation_data=(x_test_s, y_test_c), epochs=8, batch_size=64, verbose=0)
        _, acc = model.evaluate(x_test_s, y_test_c, verbose=0)
        results[name] = {'acc': float(acc), 'params': model.count_params(), 'h': h.history}

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    names = list(results.keys()); colors = ['#2196F3','#4CAF50','#FF9800']
    axes[0].bar(names, [results[n]['acc'] for n in names], color=colors)
    for i,n in enumerate(names):
        acc_val = results[n]['acc']
        axes[0].text(i, acc_val+0.01, f'{acc_val:.3f}', ha='center')
    axes[0].set_title('测试准确率', fontproperties=FONT); axes[0].set_ylim(0, 1)
    axes[1].bar(names, [results[n]['params'] for n in names], color=colors)
    for i,n in enumerate(names):
        p_val = results[n]['params']
        axes[1].text(i, p_val+3000, f'{p_val:,}', ha='center')
    axes[1].set_title('参数量', fontproperties=FONT)
    for n, c in zip(names, colors): axes[2].plot(results[n]['h']['val_accuracy'], color=c, label=n, linewidth=2)
    axes[2].set_title('验证准确率', fontproperties=FONT); axes[2].legend(prop=FONT); axes[2].grid(True, alpha=0.3)
    fig.suptitle('模型综合对比 (MNIST)', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_模型综合对比.png'); save_img(fig, p1); files.append(p1)
    exp_done(eid, d, files, {n: {'acc': results[n]['acc'], 'params': results[n]['params']} for n in names})
