#!/usr/bin/env python3
"""真实执行源码 — 15_06_动态网页抓取"""
def exp_15_6():
    """实验6: 动态网页抓取 - Selenium/Playwright基础"""
    eid = '15_06_动态网页抓取'
    d = exp_start(eid, '动态网页抓取')
    files = []

    # 图: 动态渲染流程
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.axis('off')

    flow = (
        '              静态页面 (requests)                    动态页面 (Selenium/Playwright)\n'
        '         ┌──────────────────┐                   ┌─────────────────────────┐\n'
        '         │  HTTP GET URL     │                   │  启动浏览器 (Chrome/Firefox) │\n'
        '         │       ↓           │                   │       ↓                    │\n'
        '         │  获取HTML源码     │                   │  加载页面+执行JS            │\n'
        '         │       ↓           │                   │       ↓                    │\n'
        '         │  解析/提取数据    │                   │  等待AJAX渲染完成           │\n'
        '         │       ↓           │                   │       ↓                    │\n'
        '         │  ✗ 无JS渲染      │                   │  获取完整DOM                │\n'
        '         └──────────────────┘                   │       ↓                    │\n'
        '                                                  │  提取动态加载的数据         │\n'
        '                                                  │  ✓ 完整JS渲染             │\n'
        '                                                  └─────────────────────────┘'
    )
    ax.text(0.5, 0.5, flow, ha='center', va='center', fontsize=9,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#f0f0f0'))
    ax.set_title('静态 vs 动态网页抓取', fontproperties=FONT, fontsize=14)
    p1 = os.path.join(d, '01_静态vs动态.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})
