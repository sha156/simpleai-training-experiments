#!/usr/bin/env python3
"""Ch2: TF基础知识 — 每个子图独立保存"""
import os, sys, json, time, io
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from matplotlib.font_manager import FontProperties

fm.fontManager.addfont('/tmp/simhei.ttf')
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
FONT = FontProperties(fname='/tmp/simhei.ttf')
OUT = '/tmp/out_ch2'

# ══════════ Exp1: 数据流水线与回归 ══════════
def exp1():
    d = os.path.join(OUT, '01_TF数据流水线与回归'); os.makedirs(d, exist_ok=True)
    log = io.StringIO()
    def p(s=''): print(s); log.write(s+'\n')
    files = []
    p(f'=== TF数据流水线 {time.strftime("%H:%M:%S")} ===')

    import tensorflow as tf
    np.random.seed(42)
    N = 800; X = np.random.randn(N, 3).astype(np.float32)
    y = (X[:,0]*2.5 + X[:,1]*(-1.8) + X[:,2]*0.7 + np.random.randn(N)*0.4).astype(np.float32)
    p(f'数据: X={X.shape}, y={y.shape}')

    ds = tf.data.Dataset.from_tensor_slices((X,y)).shuffle(200).batch(32).prefetch(1)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(3,)),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(4, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(tf.keras.optimizers.Adam(0.01), 'mse', ['mae'])
    h = model.fit(ds, epochs=80, verbose=0)
    final_loss = h.history['loss'][-1]
    p(f'训练完成: loss={final_loss:.6f}, mae={h.history["mae"][-1]:.6f}')

    y_pred = model.predict(X, verbose=0).flatten()
    mse = np.mean((y-y_pred)**2); mae = np.mean(np.abs(y-y_pred))
    r2 = 1 - np.sum((y-y_pred)**2)/np.sum((y-np.mean(y))**2)
    p(f'MSE={mse:.6f}, MAE={mae:.6f}, R2={r2:.6f}')

    # 图1: 训练损失曲线
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(h.history['loss'], 'b-', linewidth=2)
    ax.set_title('训练损失曲线 (MSE)', fontproperties=FONT, fontsize=14)
    ax.set_xlabel('Epoch'); ax.set_ylabel('Loss'); ax.grid(True, alpha=0.3)
    ax.annotate(f'最终Loss: {final_loss:.4f}', xy=(70, final_loss), fontsize=11, bbox=dict(facecolor='white', alpha=0.8))
    fig.tight_layout(); fig.savefig(os.path.join(d,'01_训练损失.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('01_训练损失.png')

    # 图2: 预测 vs 真实
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(y, y_pred, alpha=0.5, s=15, c='#2196F3', edgecolors='none')
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', linewidth=1.5)
    ax.set_title(f'预测 vs 真实 (R²={r2:.4f}, MAE={mae:.4f})', fontproperties=FONT, fontsize=14)
    ax.set_xlabel('真实值'); ax.set_ylabel('预测值'); ax.grid(True, alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(d,'02_预测vs真实.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('02_预测vs真实.png')

    # 图3: 数据分布 (X1-X2)
    fig, ax = plt.subplots(figsize=(10, 8))
    sc = ax.scatter(X[:,0], X[:,1], c=y, cmap='viridis', alpha=0.7, s=20, edgecolors='none')
    ax.set_title('数据分布 (X1 vs X2, 颜色=y)', fontproperties=FONT, fontsize=14)
    ax.set_xlabel('X1'); ax.set_ylabel('X2'); plt.colorbar(sc, ax=ax, label='y')
    fig.tight_layout(); fig.savefig(os.path.join(d,'03_数据分布.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('03_数据分布.png')

    # 图4: 数据分布 (X1-X3 + X2-X3)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    sc1 = axes[0].scatter(X[:,0], X[:,2], c=y, cmap='viridis', alpha=0.7, s=15, edgecolors='none')
    axes[0].set_title('X1 vs X3', fontproperties=FONT, fontsize=12); axes[0].set_xlabel('X1'); axes[0].set_ylabel('X3'); plt.colorbar(sc1, ax=axes[0])
    sc2 = axes[1].scatter(X[:,1], X[:,2], c=y, cmap='viridis', alpha=0.7, s=15, edgecolors='none')
    axes[1].set_title('X2 vs X3', fontproperties=FONT, fontsize=12); axes[1].set_xlabel('X2'); axes[1].set_ylabel('X3'); plt.colorbar(sc2, ax=axes[1])
    fig.suptitle('多维数据分布', fontproperties=FONT, fontsize=14)
    fig.tight_layout(); fig.savefig(os.path.join(d,'04_多维分布.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('04_多维分布.png')

    # 图5: 训练Loss (对数尺度)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.semilogy(h.history['loss'], 'b-', linewidth=2)
    ax.set_title('训练Loss (对数尺度)', fontproperties=FONT, fontsize=14)
    ax.set_xlabel('Epoch'); ax.set_ylabel('Loss (log)'); ax.grid(True, alpha=0.3)
    for ep in [10, 30, 60]:
        if ep < len(h.history['loss']):
            ax.annotate(f'Epoch {ep}\nLoss: {h.history["loss"][ep]:.4f}', xy=(ep, h.history["loss"][ep]),
                       xytext=(ep+10, h.history["loss"][ep]*2), arrowprops=dict(arrowstyle='->', color='red'), fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(d,'05_Loss对数.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('05_Loss对数.png')

    # 图6: 模型结构
    fig, ax = plt.subplots(figsize=(10, 6)); ax.axis('off')
    arch = (
        '┌──────────────────────────┐\n'
        '│  模型架构 (回归)          │\n'
        '│  Input(3) → Dense(16,ReLU)│\n'
        '│          → Dense(8,ReLU)  │\n'
        '│          → Dense(4,ReLU)  │\n'
        '│          → Dense(1)       │\n'
        '│                           │\n'
        f'│  参数: {model.count_params()}              │\n'
        f'│  优化器: Adam(lr=0.01)     │\n'
        f'│  损失: MSE                 │\n'
        f'│  结果: R²={r2:.4f}          │\n'
        '└──────────────────────────┘'
    )
    ax.text(0.5, 0.5, arch, ha='center', va='center', fontsize=11, fontfamily='monospace', transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='#E3F2FD', alpha=0.9))
    ax.set_title('模型结构与训练配置', fontproperties=FONT, fontsize=14)
    fig.tight_layout(); fig.savefig(os.path.join(d,'06_模型结构.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('06_模型结构.png')

    # 保存
    with open(os.path.join(d, 'code.py'), 'w', encoding='utf-8') as f:
        f.write(open(__file__, encoding='utf-8').read())
    with open(os.path.join(d, 'execution.log'), 'w', encoding='utf-8') as f:
        f.write(log.getvalue())
    result = {'files': files, 'mse': float(mse), 'mae': float(mae), 'r2': float(r2)}
    with open(os.path.join(d, 'results.json'), 'w') as f:
        json.dump({k: float(v) if isinstance(v, (np.floating, np.integer)) else v for k, v in result.items()}, f, ensure_ascii=False, indent=2)
    p(f'Exp1完成: {len(files)}张图')
    return result

# ══════════ Exp2: TensorBoard与模型可视化 ══════════
def exp2():
    d = os.path.join(OUT, '02_TensorBoard与模型可视化'); os.makedirs(d, exist_ok=True)
    log = io.StringIO()
    def p(s=''): print(s); log.write(s+'\n')
    files = []
    p(f'=== TensorBoard可视化 {time.strftime("%H:%M:%S")} ===')

    import tensorflow as tf
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32,(3,3),activation='relu',input_shape=(28,28,1),name='conv1'),
        tf.keras.layers.BatchNormalization(name='bn1'),
        tf.keras.layers.MaxPooling2D((2,2),name='pool1'),
        tf.keras.layers.Conv2D(64,(3,3),activation='relu',name='conv2'),
        tf.keras.layers.BatchNormalization(name='bn2'),
        tf.keras.layers.MaxPooling2D((2,2),name='pool2'),
        tf.keras.layers.Conv2D(64,(3,3),activation='relu',name='conv3'),
        tf.keras.layers.Flatten(name='flat'),
        tf.keras.layers.Dense(128,activation='relu',name='dense1'),
        tf.keras.layers.Dropout(0.5,name='drop'),
        tf.keras.layers.Dense(10,activation='softmax',name='output')
    ])
    sio = io.StringIO(); model.summary(print_fn=lambda x: sio.write(x+'\n')); p(sio.getvalue())
    p(f'总参数: {model.count_params():,}')

    # 图1: 模型结构表
    layer_data = [[l.name, l.__class__.__name__, str(l.output_shape).replace('None, ','').replace('(','').replace(')',''), f'{l.count_params():,}'] for l in model.layers]
    fig, ax = plt.subplots(figsize=(16, 8)); ax.axis('off')
    tbl = ax.table(cellText=layer_data, colLabels=['名称','类型','输出形状','参数'], cellLoc='center', loc='center', colWidths=[0.12,0.2,0.22,0.12])
    tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1, 1.4)
    for (r,c), cell in tbl.get_celld().items():
        if r == 0: cell.set_facecolor('#1565C0'); cell.set_text_props(color='white', fontweight='bold')
        elif r % 2 == 0: cell.set_facecolor('#E3F2FD')
    ax.set_title('CNN模型结构表', fontproperties=FONT, fontsize=14)
    fig.tight_layout(); fig.savefig(os.path.join(d,'01_模型结构表.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('01_模型结构表.png')

    # 图2: 参数分布饼图
    nonzero = [(l.name, l.count_params()) for l in model.layers if l.count_params() > 0]
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = plt.cm.tab20(np.linspace(0, 1, len(nonzero)))
    wedges, texts, autotexts = ax.pie([p for _, p in nonzero], labels=[n for n, _ in nonzero], autopct='%1.1f%%', colors=colors, textprops={'fontsize': 8})
    ax.set_title(f'参数分布 (总计 {model.count_params():,})', fontproperties=FONT, fontsize=14)
    fig.tight_layout(); fig.savefig(os.path.join(d,'02_参数分布.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('02_参数分布.png')

    # 图3: 激活函数 ReLU
    x = np.linspace(-5, 5, 200)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, np.maximum(0, x), 'b-', linewidth=2.5)
    ax.axhline(0, color='gray', linestyle=':', alpha=0.5); ax.axvline(0, color='gray', linestyle=':', alpha=0.5)
    ax.fill_between(x, np.maximum(0, x), alpha=0.2, color='blue')
    ax.set_title('ReLU激活函数: f(x)=max(0,x)', fontproperties=FONT, fontsize=14)
    ax.set_xlabel('x'); ax.set_ylabel('f(x)'); ax.grid(True, alpha=0.3)
    ax.set_xlim(-4, 4); ax.set_ylim(-1, 5)
    fig.tight_layout(); fig.savefig(os.path.join(d,'03_ReLU激活函数.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('03_ReLU激活函数.png')

    # 图4: Sigmoid
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, 1/(1+np.exp(-x)), 'g-', linewidth=2.5)
    ax.axhline(0, color='gray', linestyle=':', alpha=0.5); ax.axhline(1, color='gray', linestyle=':', alpha=0.3)
    ax.set_title('Sigmoid激活函数: f(x)=1/(1+e^-x)', fontproperties=FONT, fontsize=14)
    ax.set_xlabel('x'); ax.set_ylabel('f(x)'); ax.grid(True, alpha=0.3)
    ax.set_xlim(-4, 4); ax.set_ylim(-0.1, 1.1)
    fig.tight_layout(); fig.savefig(os.path.join(d,'04_Sigmoid激活函数.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('04_Sigmoid激活函数.png')

    # 图5: Tanh
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, np.tanh(x), 'orange', linewidth=2.5)
    ax.axhline(-1, color='gray', linestyle=':', alpha=0.3); ax.axhline(1, color='gray', linestyle=':', alpha=0.3)
    ax.set_title('Tanh激活函数: f(x)=tanh(x)', fontproperties=FONT, fontsize=14)
    ax.set_xlabel('x'); ax.set_ylabel('f(x)'); ax.grid(True, alpha=0.3)
    ax.set_xlim(-4, 4); ax.set_ylim(-1.1, 1.1)
    fig.tight_layout(); fig.savefig(os.path.join(d,'05_Tanh激活函数.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('05_Tanh激活函数.png')

    # 图6: 数据流维度变化
    dims = [28, 26, 26, 13, 11, 11, 5, 3, 3, 128, 10]
    dim_names = ['Input','Conv1','BN1','Pool1','Conv2','BN2','Pool2','Conv3','Flat','Dense1','Output']
    fig, ax = plt.subplots(figsize=(14, 6))
    colors = plt.cm.Blues(np.linspace(0.3, 0.95, len(dims)))
    ax.bar(range(len(dims)), dims, color=colors)
    ax.set_xticks(range(len(dims))); ax.set_xticklabels(dim_names, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('尺寸/维度', fontproperties=FONT)
    ax.set_title('数据流经各层的维度变化', fontproperties=FONT, fontsize=14)
    for i, v in enumerate(dims): ax.text(i, v+0.3, str(v), ha='center', fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(d,'06_维度变化.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('06_维度变化.png')

    # 图7: 各层计算量估算
    fig, ax = plt.subplots(figsize=(12, 7))
    layer_names = [l.name for l in model.layers]
    param_counts = [l.count_params() for l in model.layers]
    colors_bar = plt.cm.Greens(np.linspace(0.3, 0.9, len(layer_names)))
    ax.barh(range(len(layer_names)), param_counts, color=colors_bar)
    ax.set_yticks(range(len(layer_names))); ax.set_yticklabels(layer_names, fontsize=9)
    ax.set_xlabel('参数量', fontproperties=FONT)
    ax.set_title('各层参数量对比', fontproperties=FONT, fontsize=14)
    for i, v in enumerate(param_counts): ax.text(v+100, i, f'{v:,}', va='center', fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(d,'07_各层参数.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('07_各层参数.png')

    # 图8: MNIST样本展示
    (x_train, _), _ = tf.keras.datasets.mnist.load_data()
    sample = x_train[:10].reshape(10, 28, 28).astype('float32')/255.0
    fig, axes = plt.subplots(2, 5, figsize=(12, 5))
    for i, ax in enumerate(axes.flatten()):
        ax.imshow(sample[i], cmap='gray'); ax.axis('off')
        ax.set_title(f'样本{i+1}', fontproperties=FONT, fontsize=9)
    fig.suptitle('MNIST输入样本 (28×28灰度图)', fontproperties=FONT, fontsize=14)
    fig.tight_layout(); fig.savefig(os.path.join(d,'08_MNIST样本.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('08_MNIST样本.png')

    # 图9: 综合激活函数对比
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(x, np.maximum(0, x), 'b-', linewidth=2, label='ReLU')
    ax.plot(x, 1/(1+np.exp(-x)), 'g-', linewidth=2, label='Sigmoid')
    ax.plot(x, np.tanh(x), 'orange', linewidth=2, label='Tanh')
    ax.plot(x, np.where(x>0, x, 0.1*x), 'r--', linewidth=2, label='LeakyReLU(0.1)')
    ax.axhline(0, color='gray', linestyle=':', alpha=0.5)
    ax.set_title('常用激活函数对比', fontproperties=FONT, fontsize=14)
    ax.set_xlabel('x'); ax.set_ylabel('f(x)'); ax.legend(prop=FONT, fontsize=10); ax.grid(True, alpha=0.3)
    ax.set_xlim(-4, 4); ax.set_ylim(-1.5, 5)
    fig.tight_layout(); fig.savefig(os.path.join(d,'09_激活函数对比.png'), dpi=130, bbox_inches='tight'); plt.close(fig)
    files.append('09_激活函数对比.png')

    # 保存
    with open(os.path.join(d, 'code.py'), 'w', encoding='utf-8') as f:
        f.write(open(__file__, encoding='utf-8').read())
    with open(os.path.join(d, 'execution.log'), 'w', encoding='utf-8') as f:
        f.write(log.getvalue())
    result = {'files': files, 'total_params': int(model.count_params())}
    with open(os.path.join(d, 'results.json'), 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    p(f'Exp2完成: {len(files)}张图')
    return result

# ══════════ MAIN ══════════
os.makedirs(OUT, exist_ok=True)
r1 = exp1()
r2 = exp2()
print(f'Ch2完成: Exp1={len(r1["files"])}图, Exp2={len(r2["files"])}图')
