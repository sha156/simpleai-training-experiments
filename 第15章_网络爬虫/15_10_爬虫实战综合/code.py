#!/usr/bin/env python3
"""真实执行源码 — 15_10_爬虫实战综合"""
def exp_15_10():
    """实验10: 爬虫实战 - 综合案例"""
    eid = '15_10_爬虫实战综合'
    d = exp_start(eid, '爬虫实战综合')
    files = []

    # 爬虫完整流程图
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')

    pipeline = (
        '                        爬虫完整工作流\n'
        '   ┌─────────────────────────────────────────────────────┐\n'
        '   │  1. 种子URL ──→ 2. 请求队列 ──→ 3. DNS解析          │\n'
        '   │       │                                      │        │\n'
        '   │       ↓                                      ↓        │\n'
        '   │  4. HTTP请求 ──→ 5. 获取响应 ──→ 6. 解析HTML        │\n'
        '   │       │                                      │        │\n'
        '   │       ↓                                      ↓        │\n'
        '   │  7. 数据提取 ──→ 8. 数据清洗 ──→ 9. 数据存储        │\n'
        '   │       │                                      │        │\n'
        '   │       ↓                                      ↓        │\n'
        '   │  10. 新URL发现 ──→ 回到步骤2 ──→ ...               │\n'
        '   └─────────────────────────────────────────────────────┘'
    )
    ax.text(0.5, 0.5, pipeline, ha='center', va='center', fontsize=10,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#E3F2FD'))
    ax.set_title('爬虫实战综合案例', fontproperties=FONT, fontsize=14)

    p1 = os.path.join(d, '01_爬虫综合流程.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})
