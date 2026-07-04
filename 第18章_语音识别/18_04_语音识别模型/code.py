#!/usr/bin/env python3
"""真实执行源码 — 18_04_语音识别模型"""
def exp_18_4():
    """实验4: 语音识别模型 (HMM-GMM/CTC)"""
    eid = '18_04_语音识别模型'
    d = exp_start(eid, '语音识别模型')
    files = []

    # HMM语音识别流程
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # HMM-GMM
    axes[0].axis('off')
    axes[0].set_title('HMM-GMM传统方法', fontproperties=FONT, fontsize=12)
    hmm_flow = (
        '音频 → MFCC → GMM建模\n'
        '              ↓\n'
        '        HMM状态序列\n'
        '       (音素建模)\n'
        '              ↓\n'
        '        发音字典\n'
        '              ↓\n'
        '        语言模型\n'
        '              ↓\n'
        '         识别文本'
    )
    axes[0].text(0.5, 0.5, hmm_flow, ha='center', va='center', fontsize=9,
                 fontfamily='monospace', transform=axes[0].transAxes,
                 bbox=dict(boxstyle='round', facecolor='#E3F2FD'))

    # End-to-End
    axes[1].axis('off')
    axes[1].set_title('端到端深度学习方法', fontproperties=FONT, fontsize=12)
    e2e_flow = (
        '音频 → CNN/LSTM/Transformer\n'
        '              ↓\n'
        '        CTC/Attention\n'
        '        (序列到序列)\n'
        '              ↓\n'
        '         直接输出文本\n\n'
        '模型: DeepSpeech / Whisper\n'
        '      wav2vec / Conformer'
    )
    axes[1].text(0.5, 0.5, e2e_flow, ha='center', va='center', fontsize=9,
                 fontfamily='monospace', transform=axes[1].transAxes,
                 bbox=dict(boxstyle='round', facecolor='#E8F5E9'))

    fig.suptitle('语音识别技术演进', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_语音识别方法.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})
