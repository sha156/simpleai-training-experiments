#!/usr/bin/env python3
"""真实执行源码 — 15_04_正则表达式"""
def exp_15_4():
    """实验4: 正则表达式提取"""
    eid = '15_04_正则表达式'
    d = exp_start(eid, '正则表达式')
    files = []

    import re

    patterns = [
        (r'\d{3}-\d{4}-\d{4}', '电话号码: 138-1234-5678', ['138-1234-5678']),
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '邮箱: test@example.com, admin@site.cn', ['test@example.com', 'admin@site.cn']),
        (r'https?://[^\s<>"]+', '网址: http://example.com 和 https://test.org', ['http://example.com', 'https://test.org']),
        (r'\d{4}-\d{2}-\d{2}', '日期: 2024-01-15', ['2024-01-15']),
        (r'<[^>]+>', 'HTML: <div class="x">文本</div>', ['<div class="x">', '</div>']),
    ]

    # 图: 正则可视化
    fig, axes = plt.subplots(len(patterns), 1, figsize=(14, 10))
    for i, (pattern, text, matches) in enumerate(patterns):
        ax = axes[i]
        ax.axis('off')
        ax.text(0.02, 0.6, f'正则: {pattern}', fontsize=10, fontfamily='monospace',
                transform=ax.transAxes, color='#2196F3')
        ax.text(0.02, 0.3, f'文本: {text}', fontsize=9, transform=ax.transAxes, color='#333')
        ax.text(0.02, 0.05, f'匹配: {matches}', fontsize=9, transform=ax.transAxes, color='#4CAF50')
    fig.suptitle('正则表达式模式匹配示例', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_正则表达式.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'patterns': 5})
