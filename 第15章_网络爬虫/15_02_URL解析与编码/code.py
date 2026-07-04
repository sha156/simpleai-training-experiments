#!/usr/bin/env python3
"""真实执行源码 — 15_02_URL解析与编码"""
def exp_15_2():
    """实验2: URL解析与编码"""
    eid = '15_02_URL解析与编码'
    d = exp_start(eid, 'URL解析与编码')
    files = []

    from urllib.parse import urlparse, urlencode, quote, unquote

    # URL结构
    url = 'https://user:pass@www.example.com:8080/path/to/page?q=hello&lang=zh#section'
    parsed = urlparse(url)

    # 图: URL结构
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis('off')

    parts = [
        ('scheme', 'https', '#2196F3'),
        ('auth', 'user:pass', '#4CAF50'),
        ('host', 'www.example.com', '#FF9800'),
        ('port', '8080', '#9C27B0'),
        ('path', '/path/to/page', '#E91E63'),
        ('query', 'q=hello&lang=zh', '#00BCD4'),
        ('fragment', 'section', '#795548'),
    ]

    y = 0.8
    for name, value, color in parts:
        ax.text(0.5, y, f'{name}: {value}', ha='center', fontsize=11,
                fontfamily='monospace', transform=ax.transAxes,
                bbox=dict(facecolor=color, alpha=0.15, edgecolor=color))
        y -= 0.11

    ax.set_title('URL结构解析', fontproperties=FONT, fontsize=14)

    # URL编码示例
    examples = [
        ('空格', ' ', '%20'),
        ('中文', '你好', '%E4%BD%A0%E5%A5%BD'),
        ('特殊字符', 'a+b=c', 'a%2Bb%3Dc'),
        ('@符号', 'user@host', 'user%40host'),
    ]
    y = 0.05
    for orig, raw, encoded in examples:
        ax.text(0.5, y, f'{orig}: "{raw}" → "{encoded}"', ha='center', fontsize=9,
                fontfamily='monospace', transform=ax.transAxes, color='#666')
        y -= 0.04

    p1 = os.path.join(d, '01_URL解析.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'url_parts': dict(parsed._asdict())})
