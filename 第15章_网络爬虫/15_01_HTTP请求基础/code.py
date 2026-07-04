#!/usr/bin/env python3
"""真实执行源码 — 15_01_HTTP请求基础"""
def exp_15_1():
    """实验1: HTTP请求基础 - requests库入门"""
    eid = '15_01_HTTP请求基础'
    d = exp_start(eid, 'HTTP请求基础')
    files = []

    # 演示HTTP请求概念(不实际请求外部,避免网络问题)
    import urllib.request as ur

    # 模拟GET/POST请求
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS']
    descriptions = [
        '获取资源', '提交数据', '更新资源',
        '删除资源', '获取头部', '查询支持方法'
    ]

    # 图1: HTTP方法可视化
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.tab10(np.linspace(0, 1, len(methods)))
    y_pos = range(len(methods))[::-1]
    ax.barh(y_pos, range(len(methods), 0, -1), color=colors, alpha=0.7, height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([f'{m} - {d}' for m, d in zip(methods, descriptions)], fontproperties=FONT)
    ax.set_title('HTTP请求方法', fontproperties=FONT, fontsize=14)
    ax.set_xlabel('常见度', fontproperties=FONT)
    fig.tight_layout()
    p1 = os.path.join(d, '01_HTTP方法.png')
    save_img(fig, p1); files.append(p1)

    # 图2: HTTP请求/响应模型
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    request_flow = (
        '┌──────────────┐                    ┌──────────────┐\n'
        '│   客户端      │ ──── HTTP Request ──→ │   服务器      │\n'
        '│  (浏览器/     │                    │  (Web Server) │\n'
        '│   Python)     │ ←── HTTP Response ── │               │\n'
        '└──────────────┘                    └──────────────┘\n\n'
        'HTTP Request:\n'
        '  GET /api/data HTTP/1.1\n'
        '  Host: example.com\n'
        '  User-Agent: Python-urllib/3.x\n'
        '  Accept: application/json\n\n'
        'HTTP Response:\n'
        '  HTTP/1.1 200 OK\n'
        '  Content-Type: application/json\n'
        '  Content-Length: 253\n'
        '  \n'
        '  {"status": "success", "data": [...]}'
    )
    ax.text(0.5, 0.5, request_flow, ha='center', va='center', fontsize=10,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#f0f0f0'))
    ax.set_title('HTTP请求-响应模型', fontproperties=FONT, fontsize=14)
    p2 = os.path.join(d, '02_HTTP请求响应模型.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'methods': methods})
