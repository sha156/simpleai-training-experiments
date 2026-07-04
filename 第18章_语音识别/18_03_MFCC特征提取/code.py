#!/usr/bin/env python3
"""真实执行源码 — 18_03_MFCC特征提取"""
def exp_18_3():
    """实验3: 语音特征提取 (MFCC)"""
    eid = '18_03_MFCC特征提取'
    d = exp_start(eid, 'MFCC特征提取')
    files = []

    # MFCC计算流程可视化
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    steps = [
        ('预加重\nPre-emphasis', 'y[n]=x[n]-0.97x[n-1]'),
        ('分帧\nFraming', '25ms帧长,10ms帧移'),
        ('加窗\nWindowing', '汉明窗 Hamming'),
        ('FFT\n频谱', 'N点FFT → 功率谱'),
        ('Mel滤波\nMel Filterbank', '26个三角滤波器'),
        ('DCT\nMFCC系数', '取对数→DCT→13维'),
    ]
    for i, (title, desc) in enumerate(steps):
        ax = axes[i//3, i%3]
        ax.axis('off')
        ax.text(0.5, 0.6, title, ha='center', fontsize=12, fontproperties=FONT,
                fontweight='bold', transform=ax.transAxes)
        ax.text(0.5, 0.3, desc, ha='center', fontsize=9, fontfamily='monospace',
                transform=ax.transAxes, color='#666')
        ax.set_facecolor('#f8f8f8')
    fig.suptitle('MFCC特征提取流程', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_MFCC流程.png')
    save_img(fig, p1); files.append(p1)

    # 图2: Mel滤波器组可视化
    n_filters = 26
    n_fft = 512
    mel_points = np.linspace(0, 8000//2, n_filters + 2)
    filters = np.zeros((n_filters, n_fft//2))
    for i in range(n_filters):
        for j in range(n_fft//2):
            freq = j * 8000 / n_fft
            if freq <= mel_points[i]:
                filters[i, j] = 0
            elif freq <= mel_points[i+1]:
                filters[i, j] = (freq - mel_points[i]) / (mel_points[i+1] - mel_points[i])
            elif freq <= mel_points[i+2]:
                filters[i, j] = (mel_points[i+2] - freq) / (mel_points[i+2] - mel_points[i+1])
            else:
                filters[i, j] = 0

    fig, ax = plt.subplots(figsize=(12, 5))
    for i in range(n_filters):
        ax.plot(filters[i], linewidth=0.5, alpha=0.5)
    ax.set_title('Mel滤波器组 (26个三角滤波器)', fontproperties=FONT)
    ax.set_xlabel('频率 bin'); ax.set_ylabel('权重')
    fig.tight_layout()
    p2 = os.path.join(d, '02_Mel滤波器组.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'n_mfcc': 13, 'n_filters': 26, 'frame_ms': 25, 'hop_ms': 10})
