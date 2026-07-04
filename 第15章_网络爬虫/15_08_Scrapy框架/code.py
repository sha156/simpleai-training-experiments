#!/usr/bin/env python3
"""真实执行源码 — 15_08_Scrapy框架"""
def exp_15_8():
    """实验8: Scrapy框架基础"""
    eid = '15_08_Scrapy框架'
    d = exp_start(eid, 'Scrapy框架')
    files = []

    # 图: Scrapy架构
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')

    arch = (
        '                    Scrapy 架构\n'
        '   ┌────────────────────────────────────────────────┐\n'
        '   │              Scrapy Engine (引擎)                │\n'
        '   │    ┌──────┐   ┌──────┐   ┌──────────────┐     │\n'
        '   │    │Scheduler│←→│Downloader│←→│  Internet   │     │\n'
        '   │    │ (调度器) │   │(下载器) │   │  (互联网)    │     │\n'
        '   │    └──┬───┘   └──────┘   └──────────────┘     │\n'
        '   │       │ ↕                                       │\n'
        '   │    ┌──┴──────────┐                             │\n'
        '   │    │   Spiders    │  ← 用户编写                  │\n'
        '   │    │  (爬虫逻辑)   │                             │\n'
        '   │    └──────┬───────┘                             │\n'
        '   │           │ ↕                                    │\n'
        '   │    ┌──────┴───────┐                             │\n'
        '   │    │ Item Pipeline │  ← 数据清洗/存储             │\n'
        '   │    │  (数据管道)    │                             │\n'
        '   │    └──────────────┘                             │\n'
        '   └────────────────────────────────────────────────┘'
    )
    ax.text(0.5, 0.5, arch, ha='center', va='center', fontsize=9,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#E8F5E9'))
    ax.set_title('Scrapy爬虫框架架构', fontproperties=FONT, fontsize=14)

    p1 = os.path.join(d, '01_Scrapy架构.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})
