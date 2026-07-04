#!/usr/bin/env python3
"""真实执行源码 — 15_07_反爬虫策略"""
def exp_15_7():
    """实验7: 反爬虫策略与应对"""
    eid = '15_07_反爬虫策略'
    d = exp_start(eid, '反爬虫策略')
    files = []

    strategies = [
        ('User-Agent', '模拟浏览器标识', '重要性: ★★★★★', '#F44336'),
        ('请求频率控制', 'time.sleep() + 随机延迟', '重要性: ★★★★★', '#FF9800'),
        ('IP代理池', '轮换IP避免封禁', '重要性: ★★★★☆', '#4CAF50'),
        ('Cookie管理', '维持登录会话', '重要性: ★★★★☆', '#2196F3'),
        ('Referer设置', '模拟来源页面', '重要性: ★★★☆☆', '#9C27B0'),
        ('验证码处理', 'OCR识别/手动打码', '重要性: ★★★☆☆', '#E91E63'),
        ('JS逆向', '分析加密参数', '重要性: ★★☆☆☆', '#795548'),
    ]

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis('off')
    for i, (name, desc, importance, color) in enumerate(strategies):
        y = 0.9 - i * 0.13
        ax.text(0.05, y + 0.02, f'{i+1}. {name}', fontsize=11, fontproperties=FONT,
                fontweight='bold', color=color, transform=ax.transAxes)
        ax.text(0.4, y + 0.02, desc, fontsize=10, transform=ax.transAxes)
        ax.text(0.7, y + 0.02, importance, fontsize=9, transform=ax.transAxes, color='#888')

    ax.set_title('反爬虫策略与应对方法', fontproperties=FONT, fontsize=14)
    p1 = os.path.join(d, '01_反爬虫策略.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'strategies': len(strategies)})
