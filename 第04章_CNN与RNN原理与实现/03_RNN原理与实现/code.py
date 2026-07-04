#!/usr/bin/env python3
"""Ch4 CNN与RNN — 轻量版，逐个实验执行，不卡服务器"""
import os, sys, json, time, io, traceback
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
fm.fontManager.addfont('/tmp/simhei.ttf')
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

OUT = '/tmp/out_ch4'
os.makedirs(OUT, exist_ok=True)

def log(msg): print(f'[{time.strftime("%H:%M:%S")}] {msg}')

def save_img(fig, path):
    fig.savefig(path, dpi=120, bbox_inches='tight')
    plt.close(fig)

# ═══════════════════════════════════════════
# Exp1: CNN原理与实现
# ═══════════════════════════════════════════
def exp1():
    import tensorflow as tf
    d = os.path.join(OUT, '01_CNN原理与实现'); os.makedirs(d, exist_ok=True)
    log('Exp1: CNN — 加载MNIST...')
    (xt, yt), (xv, yv) = tf.keras.datasets.mnist.load_data()
    # 只用2000训练/500测试
    xt = xt[:2000].reshape(-1,28,28,1).astype('float32')/255.0
    xv = xv[:500].reshape(-1,28,28,1).astype('float32')/255.0
    yt_c = tf.keras.utils.to_categorical(yt[:2000], 10)
    yv_c = tf.keras.utils.to_categorical(yv[:500], 10)

    log('构建CNN...')
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16, 3, activation='relu', input_shape=(28,28,1)),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile('adam', 'categorical_crossentropy', ['accuracy'])

    log('训练(15 epochs)...')
    h = model.fit(xt, yt_c, batch_size=64, epochs=15, validation_data=(xv, yv_c), verbose=0)
    loss, acc = model.evaluate(xv, yv_c, verbose=0)
    log(f'测试准确率: {acc:.4f}')

    yp = np.argmax(model.predict(xv, verbose=0), axis=1)
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(yv[:500], yp)

    # 图1: 训练曲线
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    ax1.plot(h.history['accuracy'], 'b-', label='训练准确率')
    ax1.plot(h.history['val_accuracy'], 'b--', label='验证准确率')
    ax2.plot(h.history['loss'], 'r-', alpha=0.5, label='训练损失')
    ax2.plot(h.history['val_loss'], 'r--', alpha=0.5, label='验证损失')
    ax1.set_xlabel('Epoch'); ax1.set_ylabel('Accuracy'); ax2.set_ylabel('Loss')
    l1 = ax1.get_legend_handles_labels(); l2 = ax2.get_legend_handles_labels()
    ax1.legend(l1[0]+l2[0], l1[1]+l2[1], fontsize=8)
    ax1.set_title(f'CNN MNIST 训练 (acc={acc:.4f})', fontsize=13); ax1.grid(True, alpha=0.3)
    save_img(fig, os.path.join(d,'01_训练曲线.png'))

    # 图2: 混淆矩阵
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.imshow(cm, cmap='Blues')
    for i in range(10):
        for j in range(10):
            ax.text(j, i, cm[i,j], ha='center', va='center', fontsize=8, color='white' if cm[i,j]>cm.max()/2 else 'black')
    ax.set_xticks(range(10)); ax.set_yticks(range(10))
    ax.set_xlabel('预测'); ax.set_ylabel('真实')
    ax.set_title(f'混淆矩阵 (acc={acc:.4f})', fontsize=13)
    save_img(fig, os.path.join(d,'02_混淆矩阵.png'))

    # 图3: 样本展示
    fig, axes = plt.subplots(2, 5, figsize=(12, 5))
    for i, ax in enumerate(axes.flatten()):
        ax.imshow(xt[i].reshape(28,28), cmap='gray'); ax.axis('off')
        ax.set_title(f'数字{yt[i]}', fontsize=9)
    save_img(fig, os.path.join(d,'03_MNIST样本.png'))

    # 图4: 特征图
    fm_layer = model.layers[0]
    feat_model = tf.keras.Model(inputs=model.input, outputs=fm_layer.output)
    feat = feat_model.predict(xt[:1], verbose=0)
    fig, axes = plt.subplots(4, 4, figsize=(10, 10))
    for i in range(16):
        axes[i//4, i%4].imshow(feat[0,:,:,i], cmap='viridis'); axes[i//4, i%4].axis('off')
    save_img(fig, os.path.join(d,'04_Conv1特征图.png'))

    # 图5: 预测正确vs错误
    correct = np.where(yp == yv[:500])[0][:5]
    wrong = np.where(yp != yv[:500])[0][:5]
    fig, axes = plt.subplots(2, 5, figsize=(12, 5))
    for i in range(5):
        for row, idxs in enumerate([correct, wrong]):
            if i < len(idxs):
                idx = idxs[i]
                axes[row,i].imshow(xv[idx].reshape(28,28), cmap='gray')
                c = 'green' if row == 0 else 'red'
                axes[row,i].set_title(f'T:{yv[idx]} P:{yp[idx]}', color=c, fontsize=8)
            axes[row,i].axis('off')
    axes[0,0].set_ylabel('正确', fontsize=11); axes[1,0].set_ylabel('错误', fontsize=11)
    save_img(fig, os.path.join(d,'05_分类结果.png'))

    # 保存
    with open(os.path.join(d, 'code.py'), 'w') as f: f.write(open(__file__).read())
    with open(os.path.join(d, 'results.json'), 'w') as f: json.dump({'accuracy': float(acc)}, f)
    log(f'Exp1完成: 5张图, acc={acc:.4f}')
    return acc

# ═══════════════════════════════════════════
# Exp2: CNN NiN
# ═══════════════════════════════════════════
def exp2():
    import tensorflow as tf
    d = os.path.join(OUT, '02_CNN_NiN'); os.makedirs(d, exist_ok=True)
    log('Exp2: NiN — 加载数据...')
    (xt, yt), (xv, yv) = tf.keras.datasets.mnist.load_data()
    xt = xt[:2000].reshape(-1,28,28,1).astype('float32')/255.0
    xv = xv[:500].reshape(-1,28,28,1).astype('float32')/255.0
    yt_c = tf.keras.utils.to_categorical(yt[:2000], 10)
    yv_c = tf.keras.utils.to_categorical(yv[:500], 10)

    # NiN with 1x1 convs
    log('构建NiN...')
    nin = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16, 3, activation='relu', padding='same', input_shape=(28,28,1)),
        tf.keras.layers.Conv2D(16, 1, activation='relu'),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
        tf.keras.layers.Conv2D(32, 1, activation='relu'),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    nin.compile('adam', 'categorical_crossentropy', ['accuracy'])

    # 标准CNN对比
    std = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16, 3, activation='relu', padding='same', input_shape=(28,28,1)),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    std.compile('adam', 'categorical_crossentropy', ['accuracy'])

    log('训练NiN(12 epochs)...')
    hn = nin.fit(xt, yt_c, batch_size=64, epochs=12, validation_data=(xv, yv_c), verbose=0)
    log('训练标准CNN(12 epochs)...')
    hs = std.fit(xt, yt_c, batch_size=64, epochs=12, validation_data=(xv, yv_c), verbose=0)
    na, _ = nin.evaluate(xv, yv_c, verbose=0)
    sa, _ = std.evaluate(xv, yv_c, verbose=0)
    log(f'NiN={na:.4f}, CNN={sa:.4f}')

    # 图1: 准确率对比
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(hn.history['val_accuracy'], 'g-', lw=2, label=f'NiN (1×1conv) = {na:.4f}')
    ax.plot(hs.history['val_accuracy'], 'b-', lw=2, label=f'标准CNN = {sa:.4f}')
    ax.set_title('验证准确率对比', fontsize=13); ax.set_xlabel('Epoch'); ax.set_ylabel('Accuracy')
    ax.legend(fontsize=10); ax.grid(True, alpha=0.3)
    save_img(fig, os.path.join(d,'01_NiN_vs_CNN.png'))

    # 图2: Loss对比
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(hn.history['loss'], 'g-', label='NiN训练'); ax.plot(hn.history['val_loss'], 'g--', label='NiN验证')
    ax.plot(hs.history['loss'], 'b-', label='CNN训练'); ax.plot(hs.history['val_loss'], 'b--', label='CNN验证')
    ax.set_title('Loss对比', fontsize=13); ax.set_xlabel('Epoch'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    save_img(fig, os.path.join(d,'02_Loss对比.png'))

    # 图3: 参数量对比
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(['标准CNN', 'NiN(1×1conv)'], [std.count_params(), nin.count_params()], color=['#2196F3', '#4CAF50'])
    for b, v in zip(bars, [std.count_params(), nin.count_params()]):
        ax.text(b.get_x()+b.get_width()/2, v+500, f'{v:,}', ha='center', fontsize=12)
    ax.set_title('参数量对比', fontsize=13)
    save_img(fig, os.path.join(d,'03_参数量.png'))

    # 图4: 1×1卷积原理
    fig, ax = plt.subplots(figsize=(10, 6)); ax.axis('off')
    ax.text(0.5, 0.5, 'NiN核心: 1×1 卷积\n\n3×3 conv → 1×1 conv → 1×1 conv\n↓\n跨通道信息整合 (通道间全连接)\n增加非线性 (更多ReLU层)\n减少参数量 (vs 全连接层)', ha='center', va='center', fontsize=11, transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='#E8F5E9'))
    ax.set_title('Network in Network 原理', fontsize=14)
    save_img(fig, os.path.join(d,'04_NiN原理.png'))

    with open(os.path.join(d, 'code.py'), 'w') as f: f.write(open(__file__).read())
    with open(os.path.join(d, 'results.json'), 'w') as f: json.dump({'nin_acc': float(na), 'std_acc': float(sa)}, f)
    log(f'Exp2完成: 4张图')
    return na

# ═══════════════════════════════════════════
# Exp3: RNN原理与实现
# ═══════════════════════════════════════════
def exp3():
    import tensorflow as tf
    d = os.path.join(OUT, '03_RNN原理与实现'); os.makedirs(d, exist_ok=True)
    log('Exp3: RNN — 生成时序数据...')
    np.random.seed(42)
    t = np.linspace(0, 40, 800)
    series = np.sin(t*0.5) + 0.3*np.sin(t*1.5) + 0.05*np.random.randn(800)
    sl = 50  # sequence length
    X, y = [], []
    for i in range(len(series) - sl):
        X.append(series[i:i+sl]); y.append(series[i+sl])
    X = np.array(X[:400], dtype=np.float32).reshape(-1, sl, 1)
    y = np.array(y[:400], dtype=np.float32)
    sp = int(0.75 * len(X))
    xtr, ytr = X[:sp], y[:sp]; xte, yte = X[sp:], y[sp:]
    log(f'训练: {xtr.shape}, 测试: {xte.shape}')

    def train_rnn(layer_type):
        layers = {'simple': tf.keras.layers.SimpleRNN(16, input_shape=(sl,1)),
                  'lstm': tf.keras.layers.LSTM(16, input_shape=(sl,1)),
                  'gru': tf.keras.layers.GRU(16, input_shape=(sl,1))}
        m = tf.keras.Sequential([layers[layer_type], tf.keras.layers.Dense(1)])
        m.compile('adam', 'mse')
        m.fit(xtr, ytr, epochs=18, batch_size=32, verbose=0)
        p = m.predict(xte, verbose=0).flatten()
        return m, p, np.mean(np.abs(yte - p))

    log('训练SimpleRNN...')
    srn, ps, mas = train_rnn('simple')
    log('训练LSTM...')
    lstm, pl, mal = train_rnn('lstm')
    log('训练GRU...')
    gru, pg, mag = train_rnn('gru')
    log(f'MAE: SimpleRNN={mas:.4f}, LSTM={mal:.4f}, GRU={mag:.4f}')

    # 图1: 原始序列
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.plot(t, series, 'b-', lw=0.8, alpha=0.7)
    ax.axvline(t[sp+sl], color='r', linestyle='--', label='训练/测试分割')
    ax.set_title('时间序列 (混合正弦波)', fontsize=13); ax.legend(); ax.set_xlabel('时间'); ax.set_ylabel('值')
    save_img(fig, os.path.join(d,'01_原始序列.png'))

    # 图2: 预测对比
    n = 80
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(yte[:n], 'k-', lw=1.5, alpha=0.8, label='真实值')
    ax.plot(pl[:n], 'r-', lw=1.2, alpha=0.7, label=f'LSTM (MAE={mal:.4f})')
    ax.plot(pg[:n], 'g-', lw=1.2, alpha=0.7, label=f'GRU (MAE={mag:.4f})')
    ax.plot(ps[:n], 'orange', lw=1.2, alpha=0.7, label=f'SimpleRNN (MAE={mas:.4f})')
    ax.set_title('三种RNN预测对比', fontsize=13); ax.legend(fontsize=9); ax.grid(True, alpha=0.3)
    save_img(fig, os.path.join(d,'02_预测对比.png'))

    # 图3: RNN变体结构
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for ax, (nm, desc) in zip(axes, [
        ('SimpleRNN', 'h_t=tanh(Wx+Uh)'),
        ('LSTM', 'f/i/o 三门控\n记忆单元c_t'),
        ('GRU', '重置门+更新门\n简化版LSTM')
    ]):
        ax.axis('off'); ax.set_title(nm, fontsize=13, color='#1565C0')
        ax.text(0.5, 0.5, desc, ha='center', va='center', fontsize=10, fontfamily='monospace', transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='#F5F5F5'))
    save_img(fig, os.path.join(d,'03_RNN结构对比.png'))

    # 图4: 性能对比
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    names = ['SimpleRNN', 'LSTM', 'GRU']
    maes = [mas, mal, mag]; params = [srn.count_params(), lstm.count_params(), gru.count_params()]
    axes[0].bar(names, maes, color=['#FF9800','#F44336','#4CAF50'])
    for i, v in enumerate(maes): axes[0].text(i, v+0.003, f'{v:.4f}', ha='center', fontsize=10)
    axes[0].set_title('MAE对比', fontsize=13)
    axes[1].bar(names, params, color=['#FF9800','#F44336','#4CAF50'])
    for i, v in enumerate(params): axes[1].text(i, v+30, f'{v:,}', ha='center', fontsize=10)
    axes[1].set_title('参数量对比', fontsize=13)
    save_img(fig, os.path.join(d,'04_性能对比.png'))

    with open(os.path.join(d, 'code.py'), 'w') as f: f.write(open(__file__).read())
    with open(os.path.join(d, 'results.json'), 'w') as f: json.dump({'lstm_mae': float(mal), 'gru_mae': float(mag), 'srn_mae': float(mas)}, f)
    log(f'Exp3完成: 4张图')
    return mal

# ═══════════════════════════════════════════
# Exp4: BPTT
# ═══════════════════════════════════════════
def exp4():
    import tensorflow as tf
    d = os.path.join(OUT, '04_RNN基于时间的反向传播'); os.makedirs(d, exist_ok=True)
    log('Exp4: BPTT — 梯度分析...')

    np.random.seed(42)
    seq_lengths = [5, 10, 20, 40, 80]
    grad_norms = {}
    loss_curves = {}

    for sl in seq_lengths:
        td = np.linspace(0, 15, 300); sd = np.sin(td*0.3) + 0.1*np.random.randn(300)
        Xd, yd = [], []
        for i in range(len(sd) - sl):
            Xd.append(sd[i:i+sl]); yd.append(sd[i+sl])
        Xd = np.array(Xd[:100], dtype=np.float32).reshape(-1, sl, 1)
        yd = np.array(yd[:100], dtype=np.float32)

        m = tf.keras.Sequential([tf.keras.layers.SimpleRNN(8, input_shape=(sl, 1)), tf.keras.layers.Dense(1)])
        m.compile('adam', 'mse')
        h = m.fit(Xd, yd, epochs=12, batch_size=32, verbose=0)
        loss_curves[sl] = h.history['loss']

        with tf.GradientTape() as tape:
            pred = m(Xd[:1]); loss_val = tf.reduce_mean(tf.square(pred - yd[:1]))
        grads = tape.gradient(loss_val, m.trainable_variables)
        gn = tf.linalg.global_norm(grads).numpy()
        grad_norms[sl] = float(gn)
        log(f'  seq_len={sl}: grad_norm={gn:.6f}, loss={h.history["loss"][-1]:.6f}')

    # 图1: 梯度范数 vs 序列长度
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar([str(s) for s in seq_lengths], [grad_norms[s] for s in seq_lengths], color=plt.cm.Reds(np.linspace(0.3, 0.9, 5)))
    ax.set_title('BPTT: 序列长度 vs 梯度范数', fontsize=14); ax.set_xlabel('序列长度'); ax.set_ylabel('梯度范数')
    save_img(fig, os.path.join(d,'01_梯度范数.png'))

    # 图2: 不同序列长度训练曲线
    fig, ax = plt.subplots(figsize=(12, 5))
    for sl in seq_lengths:
        ax.plot(loss_curves[sl], lw=2, alpha=0.7, label=f'len={sl}')
    ax.set_title('不同序列长度训练曲线', fontsize=14); ax.set_xlabel('Epoch'); ax.set_ylabel('Loss')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    save_img(fig, os.path.join(d,'02_训练曲线对比.png'))

    # 图3: BPTT原理图
    fig, ax = plt.subplots(figsize=(12, 7)); ax.axis('off')
    ax.text(0.5, 0.5, 'BPTT (Through Time Backpropagation)\n\nh1→h2→...→hT (展开T层)\n∂L/∂h1 = ∂L/∂hT × Π ∂h_t/∂h_{t-1}\n\n|∂h/∂h|²<1 → 梯度指数衰减 (梯度消失)\n|∂h/∂h|²>1 → 梯度指数增长 (梯度爆炸)\n\nLSTM/GRU: 记忆单元 + 门控 = 梯度高速公路', ha='center', va='center', fontsize=9, fontfamily='monospace', transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='#FFF3E0'))
    ax.set_title('BPTT原理', fontsize=14)
    save_img(fig, os.path.join(d,'03_BPTT原理.png'))

    # 图4: 激活函数导数
    x = np.linspace(-3, 3, 200)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, np.where(x>0, 1, 0.1), 'b-', lw=2, label='ReLU导数')
    s = 1/(1+np.exp(-x)); ax.plot(x, s*(1-s), 'g-', lw=2, label='Sigmoid导数')
    t = np.tanh(x); ax.plot(x, 1-t**2, 'orange', lw=2, label='Tanh导数')
    ax.axhline(0, color='gray', linestyle=':', alpha=0.5); ax.axhline(1, color='gray', linestyle=':', alpha=0.5)
    ax.set_title('激活函数导数 (梯度乘子)', fontsize=14); ax.set_xlabel('x'); ax.set_ylabel("f'(x)")
    ax.legend(fontsize=10); ax.grid(True, alpha=0.3); ax.set_ylim(0, 1.2)
    save_img(fig, os.path.join(d,'04_激活函数导数.png'))

    with open(os.path.join(d, 'code.py'), 'w') as f: f.write(open(__file__).read())
    with open(os.path.join(d, 'results.json'), 'w') as f: json.dump({'grad_norms': grad_norms}, f)
    log(f'Exp4完成: 4张图')
    return grad_norms

# ═══════════════ MAIN ═══════════════
if __name__ == '__main__':
    log('=== Ch4 轻量版开始 ===')
    experiments = [exp1, exp2, exp3, exp4]
    for i, fn in enumerate(experiments):
        log(f'--- 实验 {i+1}/4 ---')
        try:
            fn()
            log(f'实验{i+1}完成 ✓')
        except Exception as e:
            log(f'实验{i+1}失败: {e}')
            traceback.print_exc()
        time.sleep(2)  # 给CPU喘息
    log(f'=== Ch4全部完成 {time.strftime("%H:%M:%S")} ===')
    with open(os.path.join(OUT, 'DONE'), 'w') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S'))
