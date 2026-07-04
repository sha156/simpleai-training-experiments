#!/usr/bin/env python3
"""真实执行源码 — 18_02_语音端点检测"""
def exp_18_2():
    """实验2: 语音端点检测 (VAD)"""
    eid = '18_02_语音端点检测'
    d = exp_start(eid, '语音端点检测')
    files = []

    # 模拟有语音/静音段的信号
    np.random.seed(42)
    sr = 16000
    dur = 3.0
    t = np.linspace(0, dur, int(sr * dur))
    signal = np.random.randn(len(t)) * 0.02  # 背景噪声

    # 语音段
    speech_mask = np.zeros(len(t), dtype=bool)
    speech_mask[(t > 0.5) & (t < 1.2)] = True
    speech_mask[(t > 1.8) & (t < 2.5)] = True
    signal[speech_mask] += 0.15 * np.sin(2 * np.pi * 300 * t[speech_mask])

    # 能量检测
    frame_len = int(0.025 * sr)
    energy = np.array([np.sum(signal[i:i+frame_len]**2)
                       for i in range(0, len(signal)-frame_len, frame_len//2)])
    energy_norm = energy / np.max(energy)

    # 阈值检测
    threshold = 0.1
    vad_result = energy_norm > threshold

    # 图
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))

    axes[0].plot(t, signal, 'b-', linewidth=0.5)
    axes[0].axvspan(0.5, 1.2, alpha=0.2, color='green', label='语音段')
    axes[0].axvspan(1.8, 2.5, alpha=0.2, color='green')
    axes[0].set_title('带噪声语音信号', fontproperties=FONT)
    axes[0].set_ylabel('振幅')

    t_energy = np.linspace(0, dur, len(energy))
    axes[1].plot(t_energy, energy_norm, 'r-', linewidth=1.5)
    axes[1].axhline(threshold, color='black', linestyle='--', label=f'阈值={threshold}')
    axes[1].set_title('短时能量', fontproperties=FONT)
    axes[1].set_ylabel('归一化能量'); axes[1].legend(prop=FONT)

    axes[2].plot(t_energy, vad_result.astype(int), 'g-', linewidth=2, drawstyle='steps-post')
    axes[2].set_title('VAD检测结果 (1=语音 0=静音)', fontproperties=FONT)
    axes[2].set_xlabel('时间 (秒)'); axes[2].set_ylabel('VAD'); axes[2].set_ylim(-0.1, 1.2)

    fig.suptitle('语音端点检测 (VAD)', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_VAD端点检测.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'method': 'energy_threshold', 'threshold': threshold})
