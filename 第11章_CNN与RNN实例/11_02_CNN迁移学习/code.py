#!/usr/bin/env python3
"""真实执行源码 — 11_02_CNN迁移学习"""
def exp_11_2():
    eid = '11_02_CNN迁移学习'
    d = exp_start(eid, 'CNN迁移学习')
    files = []
    import tensorflow as tf
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train = x_train[:2000].astype('float32')/255.0; x_test_s = x_test[:500].astype('float32')/255.0
    x_train_rgb = np.stack([x_train]*3, axis=-1); x_test_rgb = np.stack([x_test_s]*3, axis=-1)
    x_train_rgb = tf.image.resize(x_train_rgb, (32,32)).numpy(); x_test_rgb = tf.image.resize(x_test_rgb, (32,32)).numpy()
    y_train_c = tf.keras.utils.to_categorical(y_train[:2000], 10); y_test_c = tf.keras.utils.to_categorical(y_test[:500], 10)

    m1 = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16,3,activation='relu',input_shape=(32,32,3)),
        tf.keras.layers.MaxPooling2D(2), tf.keras.layers.Conv2D(32,3,activation='relu'),
        tf.keras.layers.GlobalAveragePooling2D(), tf.keras.layers.Dense(10,activation='softmax')
    ]); m1.compile('adam','categorical_crossentropy',['accuracy'])
    h1 = m1.fit(x_train_rgb, y_train_c, validation_data=(x_test_rgb, y_test_c), epochs=15, batch_size=64, verbose=0)

    m2 = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32,3,activation='relu',input_shape=(32,32,3)),
        tf.keras.layers.Conv2D(32,3,activation='relu'), tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Conv2D(64,3,activation='relu'), tf.keras.layers.Conv2D(64,3,activation='relu'),
        tf.keras.layers.GlobalAveragePooling2D(), tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64,activation='relu'), tf.keras.layers.Dense(10,activation='softmax')
    ]); m2.compile('adam','categorical_crossentropy',['accuracy'])
    h2 = m2.fit(x_train_rgb, y_train_c, validation_data=(x_test_rgb, y_test_c), epochs=15, batch_size=64, verbose=0)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(h1.history['val_accuracy'], 'b-', label='轻量模型', linewidth=2)
    ax.plot(h2.history['val_accuracy'], 'r-', label='深层模型', linewidth=2)
    ax.set_title('验证准确率对比', fontproperties=FONT); ax.legend(prop=FONT); ax.grid(True, alpha=0.3)
    fig.tight_layout()
    p1 = os.path.join(d, '01_迁移学习对比.png'); save_img(fig, p1); files.append(p1)
    exp_done(eid, d, files, {'light_acc': float(h1.history['val_accuracy'][-1]), 'deep_acc': float(h2.history['val_accuracy'][-1])})
