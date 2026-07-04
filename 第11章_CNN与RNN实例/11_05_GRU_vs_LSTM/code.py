#!/usr/bin/env python3
"""真实执行源码 — 11_05_GRU_vs_LSTM"""
def exp_11_5():
    eid = '11_05_GRU_vs_LSTM'
    d = exp_start(eid, 'GRU vs LSTM')
    files = []
    import tensorflow as tf
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.imdb.load_data(num_words=3000)
    x_train = tf.keras.preprocessing.sequence.pad_sequences(x_train[:1500], maxlen=150)
    x_test_s = tf.keras.preprocessing.sequence.pad_sequences(x_test[:400], maxlen=150)

    def bm(t):
        l = tf.keras.layers.LSTM(32, dropout=0.2) if t=='lstm' else tf.keras.layers.GRU(32, dropout=0.2)
        m = tf.keras.Sequential([tf.keras.layers.Embedding(3000,32,input_length=150), l, tf.keras.layers.Dense(1,activation='sigmoid')])
        m.compile('adam','binary_crossentropy',['accuracy']); return m

    hl = bm('lstm').fit(x_train, y_train[:1500], validation_data=(x_test_s, y_test[:400]), epochs=8, batch_size=64, verbose=0)
    hg = bm('gru').fit(x_train, y_train[:1500], validation_data=(x_test_s, y_test[:400]), epochs=8, batch_size=64, verbose=0)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, m in zip(axes, ['val_accuracy','val_loss']):
        ax.plot(hl.history[m], 'b-o', markersize=4, label='LSTM')
        ax.plot(hg.history[m], 'r-s', markersize=4, label='GRU')
        ax.set_title('验证准确率' if 'acc' in m else '验证损失', fontproperties=FONT); ax.legend(prop=FONT); ax.grid(True, alpha=0.3)
    fig.suptitle('LSTM vs GRU (IMDB)', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_LSTM_vs_GRU.png'); save_img(fig, p1); files.append(p1)
    exp_done(eid, d, files, {'lstm_acc': float(hl.history['val_accuracy'][-1]), 'gru_acc': float(hg.history['val_accuracy'][-1])})
