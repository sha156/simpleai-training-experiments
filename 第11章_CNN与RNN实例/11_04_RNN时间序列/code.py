#!/usr/bin/env python3
"""真实执行源码 — 11_04_RNN时间序列"""
def exp_11_4():
    eid = '11_04_RNN时间序列'
    d = exp_start(eid, 'RNN时间序列')
    files = []
    import tensorflow as tf
    np.random.seed(42)
    t = np.linspace(0, 50, 800)
    series = np.sin(t) + 0.1 * np.random.randn(800)
    X, y = [], []
    for i in range(len(series) - 50):
        X.append(series[i:i+50]); y.append(series[i+50])
    X, y = np.array(X), np.array(y)
    sp = int(0.8*len(X))
    X_tr, y_tr = X[:sp].reshape(-1,50,1), y[:sp]
    X_te, y_te = X[sp:].reshape(-1,50,1), y[sp:]

    model = tf.keras.Sequential([tf.keras.layers.LSTM(32, input_shape=(50,1)), tf.keras.layers.Dense(1)])
    model.compile('adam','mse'); model.fit(X_tr, y_tr, validation_data=(X_te, y_te), epochs=20, batch_size=32, verbose=0)
    preds = model.predict(X_te, verbose=0).flatten()

    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    axes[0].plot(t, series, 'b-', linewidth=1, alpha=0.7)
    axes[0].axvline(t[sp+50], color='r', linestyle='--', label='训练/测试分割')
    axes[0].set_title('正弦波序列', fontproperties=FONT); axes[0].legend(prop=FONT)
    axes[1].plot(y_te[:150], 'b-', linewidth=1, alpha=0.6, label='真实')
    axes[1].plot(preds[:150], 'r-', linewidth=1.5, alpha=0.8, label='LSTM预测')
    axes[1].set_title(f'预测结果 (MAE={np.mean(np.abs(y_te-preds)):.4f})', fontproperties=FONT); axes[1].legend(prop=FONT)
    fig.suptitle('LSTM时间序列预测', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_LSTM时间序列.png'); save_img(fig, p1); files.append(p1)
    exp_done(eid, d, files, {'mae': float(np.mean(np.abs(y_te-preds)))})
