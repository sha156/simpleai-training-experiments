#!/usr/bin/env python3
"""真实执行源码 — 18_01_语音信号基础"""
def exp_18_1():
    """实验1: 语音信号基础 - 波形与频谱"""
    eid = '18_01_语音信号基础'
    d = exp_start(eid, '语音信号基础')
    files = []

    # 生成模拟音频信号
    np.random.seed(42)
    sr = 16000
    duration = 2.0
    t = np.linspace(0, duration, int(sr * duration))

    # 复合信号: 基频 + 谐波 + 噪声
    signal = (0.5 * np.sin(2 * np.pi * 440 * t) +
              0.3 * np.sin(2 * np.pi * 880 * t) +
              0.15 * np.sin(2 * np.pi * 1320 * t) +
              0.05 * np.random.randn(len(t)))

    # STFT
    from scipy import signal as scisig
    f, t_spec, Zxx = scisig.stft(signal, sr, nperseg=256)

    # 图1: 波形
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))

    axes[0].plot(t[:1000], signal[:1000], 'b-', linewidth=0.5)
    axes[0].set_title('语音波形 (440Hz基频+谐波+噪声)', fontproperties=FONT)
    axes[0].set_xlabel('时间 (秒)'); axes[0].set_ylabel('振幅')

    # 频谱图
    im = axes[1].pcolormesh(t_spec, f[:128], np.abs(Zxx[:128]), shading='gouraud', cmap='magma')
    axes[1].set_title('语谱图 (STFT)', fontproperties=FONT)
    axes[1].set_xlabel('时间 (秒)'); axes[1].set_ylabel('频率 (Hz)')
    plt.colorbar(im, ax=axes[1], label='幅度')

    fig.suptitle('语音信号分析基础', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_语音信号分析.png')
    save_img(fig, p1); files.append(p1)

    # 图2: MFCC模拟
    n_mfcc = 13
    mfcc_sim = np.random.randn(n_mfcc, len(t_spec)) * np.exp(-np.arange(n_mfcc)[:, None] / 3)

    fig, ax = plt.subplots(figsize=(12, 5))
    im = ax.imshow(mfcc_sim, aspect='auto', cmap='viridis')
    ax.set_title(f'MFCC特征模拟 ({n_mfcc}维)', fontproperties=FONT)
    ax.set_xlabel('帧索引'); ax.set_ylabel('MFCC系数')
    plt.colorbar(im, ax=ax)
    fig.tight_layout()
    p2 = os.path.join(d, '02_MFCC模拟.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'sample_rate': sr, 'duration': duration})
