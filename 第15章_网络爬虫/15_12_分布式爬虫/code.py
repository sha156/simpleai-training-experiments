#!/usr/bin/env python3
"""真实执行源码 — 15_12_分布式爬虫"""
def exp_15_12():
    """实验12: 分布式爬虫概念"""
    eid = '15_12_分布式爬虫'
    d = exp_start(eid, '分布式爬虫')
    files = []

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.axis('off')

    arch = (
        '                      分布式爬虫架构\n'
        '   ┌──────────────────────────────────────────────────────┐\n'
        '   │                   Redis (URL队列/去重)                 │\n'
        '   │              ┌───────────┬───────────┐                │\n'
        '   │              ↓           ↓           ↓                │\n'
        '   │         ┌─────────┐ ┌─────────┐ ┌─────────┐          │\n'
        '   │         │ Worker1 │ │ Worker2 │ │ Worker3 │  ...     │\n'
        '   │         │ (爬虫)  │ │ (爬虫)  │ │ (爬虫)  │          │\n'
        '   │         └────┬────┘ └────┬────┘ └────┬────┘          │\n'
        '   │              ↓           ↓           ↓                │\n'
        '   │         ┌──────────────────────────────────┐          │\n'
        '   │         │        MongoDB/MySQL (存储)        │          │\n'
        '   │         └──────────────────────────────────┘          │\n'
        '   └──────────────────────────────────────────────────────┘\n'
        '   组件: Scrapy-Redis / Celery / RabbitMQ / Kafka'
    )
    ax.text(0.5, 0.5, arch, ha='center', va='center', fontsize=9,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#F3E5F5'))
    ax.set_title('分布式爬虫架构', fontproperties=FONT, fontsize=14)

    p1 = os.path.join(d, '01_分布式爬虫.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})
