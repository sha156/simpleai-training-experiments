#!/usr/bin/env python3
"""真实执行源码 — 18_05_语音合成"""
def exp_18_5():
    """实验5: 语音合成基础 (TTS)"""
    eid = '18_05_语音合成'
    d = exp_start(eid, '语音合成')
    files = []

    # TTS流程
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].axis('off')
    tts_flow = (
        '        文本到语音 (TTS) 流程\n\n'
        '   文本输入: "你好世界"\n'
        '        ↓\n'
        '   文本分析: 分词/注音/韵律预测\n'
        '        ↓\n'
        '   声学模型: 文本→声学特征\n'
        '   (Tacotron2 / FastSpeech)\n'
        '        ↓\n'
        '   声码器: 声学特征→波形\n'
        '   (WaveNet / HiFi-GAN)\n'
        '        ↓\n'
        '   音频输出: 合成语音波形'
    )
    axes[0].text(0.5, 0.5, tts_flow, ha='center', va='center', fontsize=9,
                 fontfamily='monospace', transform=axes[0].transAxes,
                 bbox=dict(boxstyle='round', facecolor='#F3E5F5'))

    # 不同TTS方法对比
    methods = ['拼接合成', '参数合成\n(HMM)', '深度学习\n(Tacotron)', '端到端\n(FastSpeech2)']
    quality = [2, 3, 4.5, 4.8]
    naturalness = [2, 2.5, 4, 4.5]
    colors = ['#F44336', '#FF9800', '#4CAF50', '#2196F3']

    x = np.arange(len(methods))
    w = 0.3
    axes[1].bar(x - w/2, quality, w, label='质量', color=colors, alpha=0.8)
    axes[1].bar(x + w/2, naturalness, w, label='自然度', color=colors, alpha=0.4)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(methods, fontproperties=FONT, fontsize=9)
    axes[1].set_title('TTS方法对比 (5分制)', fontproperties=FONT)
    axes[1].set_ylim(0, 5.5)
    axes[1].legend(prop=FONT)

    fig.suptitle('语音合成 (TTS) 技术', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_TTS技术.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})


# ══════════════════════════════════════════════════════════════
#  第19章: 区块链 (17个实验) - 本地运行
# ══════════════════════════════════════════════════════════════
