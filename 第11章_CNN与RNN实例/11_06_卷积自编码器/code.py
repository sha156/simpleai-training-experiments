#!/usr/bin/env python3
"""真实执行源码 — 11_06_卷积自编码器"""
def fix_11_06():
    """卷积自编码器 - 修复版"""
    d = OUT_DIRS[1]
    files = []
    import tensorflow as tf
    (x_train, _), (x_test, _) = tf.keras.datasets.mnist.load_data()
    x_train = x_train[:2000].reshape(-1,28,28,1).astype('float32')/255.0
    x_test_s = x_test[:20].reshape(-1,28,28,1).astype('float32')/255.0

    inp = tf.keras.layers.Input(shape=(28,28,1))
    e = tf.keras.layers.Conv2D(16,3,activation='relu',padding='same')(inp)
    e = tf.keras.layers.MaxPooling2D(2,padding='same')(e)
    e = tf.keras.layers.Conv2D(8,3,activation='relu',padding='same')(e)
    encoded = tf.keras.layers.MaxPooling2D(2,padding='same')(e)
    de = tf.keras.layers.Conv2D(8,3,activation='relu',padding='same')(encoded)
    de = tf.keras.layers.UpSampling2D(2)(de)
    de = tf.keras.layers.Conv2D(16,3,activation='relu',padding='same')(de)
    de = tf.keras.layers.UpSampling2D(2)(de)
    decoded = tf.keras.layers.Conv2D(1,3,activation='sigmoid',padding='same')(de)
    ae = tf.keras.Model(inp, decoded); ae.compile('adam','binary_crossentropy')
    ae.fit(x_train, x_train, epochs=12, batch_size=64, validation_data=(x_test_s, x_test_s), verbose=0)
    dec = ae.predict(x_test_s, verbose=0)

    fig, axes = plt.subplots(2, 10, figsize=(18, 4))
    for i in range(10):
        axes[0,i].imshow(x_test_s[i].reshape(28,28), cmap='gray'); axes[0,i].axis('off')
        axes[1,i].imshow(dec[i].reshape(28,28), cmap='gray'); axes[1,i].axis('off')
        if i == 0: axes[0,i].set_title('原图', fontproperties=FONT, fontsize=8)
        if i == 0: axes[1,i].set_title('重建', fontproperties=FONT, fontsize=8)
    fig.suptitle('卷积自编码器 — 原图 vs 重建', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p = os.path.join(d, '01_自编码器重建.png')
    save_img(fig, p); files.append(p)

    with open(os.path.join(d, 'results.json'), 'w') as f:
        json.dump({'files': files}, f)
    print(f'11_06: {len(files)} files OK')
