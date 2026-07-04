#!/usr/bin/env python3
"""真实执行源码 — 15_09_数据存储"""
def exp_15_9():
    """实验9: 数据存储 - MySQL/MongoDB基础"""
    eid = '15_09_数据存储'
    d = exp_start(eid, '数据存储')
    files = []

    # 图: 存储方案对比
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis('off')

    storage = [
        ('MySQL/PostgreSQL', '关系型数据库', '结构化数据、关联查询', '爬虫结果、用户信息'),
        ('MongoDB', '文档型NoSQL', 'JSON直接存储、灵活Schema', '非结构化数据、日志'),
        ('Redis', '键值存储/缓存', '极快读写、去重、队列', 'URL去重、请求队列'),
        ('CSV/Excel', '文件存储', '简单直接、通用性强', '小批量数据导出'),
        ('JSON文件', '文本存储', '人类可读、易于版本管理', '配置、中间结果'),
    ]

    for i, (name, typ, feature, use_case) in enumerate(storage):
        y = 0.85 - i * 0.17
        ax.text(0.05, y, f'{name}', fontsize=11, fontproperties=FONT, fontweight='bold',
                color='#2196F3', transform=ax.transAxes)
        ax.text(0.3, y, f'类型: {typ}', fontsize=9, transform=ax.transAxes)
        ax.text(0.55, y, f'特点: {feature}', fontsize=9, transform=ax.transAxes)
        ax.text(0.8, y, f'场景: {use_case}', fontsize=9, transform=ax.transAxes, color='#666')

    ax.set_title('爬虫数据存储方案对比', fontproperties=FONT, fontsize=14)
    p1 = os.path.join(d, '01_数据存储方案.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})
